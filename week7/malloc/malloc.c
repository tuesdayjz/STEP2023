//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head;
  my_metadata_t dummy;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
#define BIN_SLOT 512
my_heap_t bins[BIN_SLOT];
//
// Helper functions (feel free to add/remove/edit!)
//

// if size is bigger than 4096, put it in the last bin
// else, put it in the bin that size is divided by 4096/BIN_SLOT
int get_bin_num(size_t size) {
  if (size > 4096) {
    return BIN_SLOT - 1;
  } else {
    return size / (4096 / BIN_SLOT);
  }
}

void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  int bin_num = get_bin_num(metadata->size);
  metadata->next = bins[bin_num].free_head;
  bins[bin_num].free_head = metadata;
}

void merge_free_list(my_metadata_t *metadata) {
  // merge if it has adjacent free block
  int bin_num = get_bin_num(metadata->size);
  bool is_merged = false;
  my_metadata_t *cur = bins[bin_num].free_head;
  my_metadata_t *prev = NULL;
  while (cur) { // search adjacent free block from the first bin to the last bin
    if (prev && ((my_metadata_t *)((char *)prev + prev->size) == cur)) {
      // if prev + prev->size is same as cur, merge
      my_metadata_t *next = cur->next;
      prev->size += cur->size;
      prev->next = next;
      cur = next;
      is_merged = true;
    } else { // if not, move to next
      prev = cur;
      cur = cur->next;
    }
  }
  if (is_merged) {
    move_large_block(prev);
  }
}

void move_large_block (my_metadata_t *metadata){
  // move large block to other list
  int bin_num = get_bin_num(metadata->size);
  int bin_size = 4096 / BIN_SLOT;
  // search free block
  // if block is bigger than expected size, move to other list
  my_metadata_t *cur = bins[bin_num].free_head;
  my_metadata_t *prev = NULL;
  while (cur) {
    if (cur->size >= (bin_num + 1) * bin_size && cur != metadata) {
      if (prev) {
        prev->next = cur->next;
      } else {
        bins[bin_num].free_head = cur->next;
      }
      cur->next = NULL;
      my_add_to_free_list(cur);
      break;
    } else {
      prev = cur;
      cur = cur->next;
    }
  }
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    int bin_num = get_bin_num(metadata->size);
    bins[bin_num].free_head = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  bins[0].dummy.size = 0;
  bins[0].dummy.next = NULL;
  for (int i = 0; i < BIN_SLOT; i++) {
    bins[i].free_head = &bins[0].dummy;
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  // First-fit: Find the first free slot the object fits.
  // TODO: Update this logic to Best-fit!

  int bin_num = get_bin_num(size);
  my_metadata_t *metadata = NULL;
  my_metadata_t *prev = NULL;
  my_metadata_t *best_metadata = NULL;
  my_metadata_t *best_prev = NULL;

  // search data from desired bin to the last bin
  for (int i = bin_num; i < BIN_SLOT; i++) {
    metadata = bins[i].free_head;
    prev = NULL;
    // if metadata size is smaller than size, go to next metadata
    if (metadata && metadata->size < size) {
      prev = metadata;
      metadata = metadata->next;
    } else if (metadata) {
      best_prev = prev;
      best_metadata = metadata;
      break;
    }
  }

  // best-fit:
  while (metadata) {
    if (metadata->size > size && (!best_metadata || best_metadata->size > metadata->size)) {
      best_metadata = metadata;
      best_prev = prev;
    }
    prev = metadata;
    metadata = metadata->next;
  }
  metadata = best_metadata;
  prev = best_prev;

  /*
    // worst-fit:
    my_metadata_t *worst_metadata = NULL;
    my_metadata_t *worst_prev = NULL;
    while (metadata) {
      if (metadata->size >= size && (!worst_metadata || worst_metadata->size <
    metadata->size)) { worst_metadata = metadata; worst_prev = prev;
      }
      prev = metadata;
      metadata = metadata->next;
    }
    metadata = worst_metadata;
    prev = worst_prev;
  */

  // now, metadata points to the first free slot
  // and prev is the previous entry.

  if (!metadata) {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    // Add the memory region to the free list.
    my_add_to_free_list(metadata);
    // merge_free_list(metadata);
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  // Remove the free slot from the free list.
  my_remove_from_free_list(metadata, prev);

  if (remaining_size > sizeof(my_metadata_t)) {
    // Shrink the metadata for the allocated object
    // to separate the rest of the region corresponding to remaining_size.
    // If the remaining_size is not large enough to make a new metadata,
    // this code path will not be taken and the region will be managed
    // as a part of the allocated object.
    metadata->size = size;
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    metadata->size = size;
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata);
    // merge_free_list(new_metadata);
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // Add the free slot to the free list.
  my_add_to_free_list(metadata);
  // merge_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
