from typing import List
import time


def Timer(func):
    """Print the runtime of the decorated function"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        run_time = time.time() - start_time
        print(f"Finished {func.__name__!r} in {run_time:.10f} secs")
    return wrapper


class Sort(object):
    def __init__(self, dataset:list):
        self.unsorted_list = dataset.copy()
        self.sorted_list = dataset.copy()

    def bubble_sort(self):
        """Sort array using Bubblesort"""
        #print ("Bubble sort")
        for a1 in range (len(self.sorted_list)-1):
            for a in range (len(self.sorted_list)-1):
                v1 = self.sorted_list[a]; v2 = self.sorted_list[a+1]
                if v1 > v2:
                    self.sorted_list[a]=v2
                    self.sorted_list[a+1] = v1

    def merge_sort(self, l1:list):
        """Sort array using mergesort"""
        #print ("Merge sort")
        if len(l1) > 1:
            mid = len(l1) // 2
            left_l = l1[:mid]
            right_l = l1[mid:]
            self.merge_sort(left_l)
            self.merge_sort(right_l)

            i=0; j=0; k=0;
            while i < len(left_l) and j < len(right_l):
                if left_l[i] < right_l[j]:
                    l1[k] = left_l[i]
                    i += 1
                else:
                    l1[k] = right_l[j]
                    j += 1
                k += 1

            while i < len(left_l):
                l1[k] = left_l[i]
                i += 1
                k += 1

            while j < len(right_l):
                l1[k] = right_l[j]
                j += 1
                k += 1

        self.sorted_list = l1

    def quick_sort(self, dataset: list, first: int, last: int):
        """Sort array using Quicksort"""
        # print("first %i, last %i, %s:)" %(first, last, dataset))
        # so long as first < last create a pivot index and sort the two lower and upper portion of the dataset around the pivot value
        if first < last:
            pivot_val = dataset[first]

            lower = first + 1
            upper = last

            while upper >= lower:
                while lower <= upper and dataset[lower] <= pivot_val:
                    lower += 1
                while upper >= lower and dataset[upper] >= pivot_val:
                    upper -= 1

                if upper > lower: # perform swap
                    dataset[lower], dataset[upper] = dataset[upper], dataset[lower]

            # swap our pivot index with the upper
            pivot_idx = upper
            dataset[first], dataset[pivot_idx] = dataset[pivot_idx], dataset[first]

            # sort the two portions of the dataset array leaving the pivot as is in the array
            self.quick_sort(dataset, first, pivot_idx-1)
            self.quick_sort(dataset, pivot_idx+1, last)

        self.sorted_list = dataset

    def radix_sort (self, tenths_pos:int = 0):
        """Sort array using Radixsort"""

        # create list of position digits where the index is the same as the 'sorted list'
        tenths_digits = [(0 if n < 10 ** tenths_pos else 1) for n in self.sorted_list]
        if sum(tenths_digits) == 0: # out of 10ths position digit - we are done
            return
        pos_val_list = [(0 if n<10**tenths_pos else (int(str(n)[::-1][tenths_pos]))) for n in self.sorted_list]

        # inplace insertion-sort of pos_val_list (AND self.sorted_list)
        # take the first unsorted item and place it in the correct place in the sorted portion
        unsort_list_idx = 1
        while unsort_list_idx < len(self.sorted_list):
            j = unsort_list_idx
            while j: # j is the idx to the last+1 of the sorted list portion
                # if first number of the unsorted portion of the list, indexed by  unsort_list_iex is
                # < a number in the sorted portion of the list, swap it (and swap the self.sorted_list
                # using the same index.
                if pos_val_list[j] < pos_val_list[j-1]:
                    pos_val_list[j-1], pos_val_list[j] = pos_val_list[j], pos_val_list[j-1]
                    self.sorted_list[j-1], self.sorted_list[j] = self.sorted_list[j], self.sorted_list[j-1]
                else: # if current unsorted number is not < largest sorted then move on
                    break
                j -= 1
            unsort_list_idx += 1
        tenths_pos +=1 # move to the next 10s position
        self.radix_sort(tenths_pos)

    def print(self):
        print("unsorted:", self.unsorted_list)
        print("sorted:", self.sorted_list)


class Heap_sort(object):
    """ sort array using max heap sort"""

    def __init__(self, arr: list):
        ''' 1) The heap will hold the root node in heap[0], each odd element node is 2*element+1, even element nodes
               are in 2*element+2
            2) Heap trees are 'complete' meaning all elements are filled in left to right, top to bottom. That is,
               there are no gaps in the tree.
            3) This is a 'max heap' so all parents must be > than all childen (fix() fixes the last element added
               (The root element always holds the largest value in the heap after the heap is fixed)
        '''
        self.heap=[]
        # initialize heap with the passed in array
        for elem in arr:
            self.add_element(elem)


    def add_element(self, element:int):
        """ add element to heap

            When adding an element we always add to the end of the heap and then fix the heap.
        """
        self.heap.append(element)
        # fix heap starting from the end (element we just added)
        idx = len(self.heap)-1
        while idx !=0:
            parent_idx = int((idx-1)/2) if idx%2 else int(idx/2)-1
            #print("before swap ( %i, %i ): %s" %(idx, parent_idx, self.heap))
            if self.heap[idx] > self.heap[parent_idx]:
                #print("swap")
                self.heap[idx], self.heap[parent_idx] = self.heap[parent_idx], self.heap[idx]
                #print ("after swap: ", self.heap)
            idx = parent_idx

    def remove_element(self, heap:list) -> float:
        """ remove root element from heap

            When removing the root, we always replace the root with the last element in the heap and
            then fix the heap. To fix the heap from the top, we swap (if the root is smaller) the larger of the
            children and follow that path until no more children..
        """

        rtn_val = heap[0]
        heap[0] = heap.pop()  # replace the root with the last element in the heap

        # fix heap starting from the top
        idx, child_l_idx, child_r_idx = 0, 0, 0
        if len(heap) > 1:
            child_l_idx = 1
        if len(heap) > 2:
            child_r_idx = 2

        while child_l_idx or child_r_idx:
                # print ("temp_heap: %s\n, idx=%i, child_l_idx: %i, child_r_idx: %i" %(heap, idx, child_l_idx, child_r_idx))
                l_val = heap[child_l_idx] if child_l_idx else 0
                r_val = heap[child_r_idx] if child_r_idx else 0

                # we know we have at least one child so assign the index of the larger to child_idx
                child_idx =  child_l_idx if l_val > r_val else child_r_idx
                if heap[idx] > heap[child_idx]:
                    break # child was smaller so we are done

                # child was larger so swap and keep checking
                heap[idx], heap[child_idx] = heap[child_idx], heap[idx]
                idx = child_idx
                child_l_idx = idx * 2 + 1 if (len(heap)-1) >= idx * 2 + 1 else 0
                child_r_idx = idx * 2 + 2 if (len(heap)-1) >= idx * 2 + 2 else 0
        # exiting this while statement we have a 'complete' and correct heap after removal

        return rtn_val

    def print_ordered(self):
        """ print the heap from largest to smallest
            Note: This requires we remove the max element[0] recursively until done

        """
        temp_heap = self.heap.copy() # our process destroys the heap so we need a copy to work with
        arr = []

        while len(temp_heap) > 1:
            arr.append(self.remove_element(temp_heap))

        arr.append(temp_heap[0])  # pick off the last element
        print ("'Correct and complete' Heap Array:", self.heap)
        print ("Printed - ordered descending:", arr)

@Timer
def run_bubble_sort(obj):
    obj.bubble_sort()


@Timer
def run_merge_sort(obj):
    obj.merge_sort(obj.sorted_list)  # inplace sort so use the 'sorted_list' copy of unsorted in c'tor

@Timer
def run_quick_sort(obj):             # inplace sort so use the 'sorted_list' copy of unsorted in c'tor
    obj.quick_sort(obj.sorted_list, 0, len(obj.sorted_list)-1)

@Timer
def run_radix_sort(obj):             # inplace sort so use the 'sorted_list' copy of unsorted in c'tor
    obj.radix_sort()

def main():
    l = [503, 6, 200, 8, 109, 506, 203, 807, 401, 409, 100,  4, 6, 900, 1200, 5, 207, 503, 6, 200, 8, 109, 506, 203, 807, 401, 409, 100, 4, 6, 900, 1200, 5, 207]

    b_sort = Sort(l)
    run_bubble_sort(b_sort)
    b_sort.print()

    m_sort = Sort(l)
    run_merge_sort(m_sort)
    m_sort.print()

    q_sort = Sort(l)
    run_quick_sort(q_sort)
    q_sort.print()

    r_sort = Sort(l)
    run_radix_sort(r_sort)
    r_sort.print()

    print ("Makes no sense to time a Heap sort")
    h_sort = Heap_sort(l)
    h_sort.print_ordered()


if __name__ == "__main__":
    main()
