//name:ZANNING WANG
//ID:z5224151
//test on mac
//I only finish part of this assignment, the TaskScheduler does not work, therefore I delete this part of code and
//test other part of code in the main{}.
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>

// data type for heap nodes
typedef struct HeapNode { 
	// each node stores the priority (key), name, execution time,
	//  release time and deadline of one task
	int key; //key of this task
	int TaskName;  //task name 
	int Etime; //execution time of this task
	int Rtime; // release time of this task
	int Dline; // deadline of this task
	int degree; // degree of the heapnode
	struct HeapNode *parent;
	struct HeapNode *child;
	struct HeapNode *sibling;
} HeapNode;

//data type for a priority queue (heap) 
typedef struct BinomialHeap{ //this is heap header
	int  size;      // count of items in the heap
	HeapNode *head;
} BinomialHeap;

// create a new heap node to store an item (task) 
HeapNode *newHeapNode(int k, int n, int c, int r, int d)
{ // k:key, n:task name, c: execution time, r:release time, d:deadline
  // ... you need to define other parameters yourself) 	 
	HeapNode *new;
	new = malloc(sizeof(HeapNode));
	assert(new != NULL);
	new->key = k;
	new->TaskName = n;
	new->Etime = c;
	new->Rtime = r; 
	new->Dline = d;
	new->degree = 0;
	new->parent = NULL;
	new->child = NULL;
	new->sibling = NULL;
	return new;
}

// create a new empty heap-based priority queue
BinomialHeap *newHeap()
{ // this function creates an empty binomial heap-based priority queue
	BinomialHeap *T;
	T = malloc(sizeof(BinomialHeap));
	assert (T != NULL);
	T->size = 0;
	T->head = NULL;
	return T;
}

//declare the function used
//This function is used to merge two heap into one and sorted the heap according to the degree
static BinomialHeap *heap_merge(BinomialHeap *h1, BinomialHeap *h2)
{

    BinomialHeap *T = newHeap();
    //use head
    HeapNode *head = NULL;
    HeapNode **pos = &head;
    //use the pos to store the node in the new heap
    T->size = h1->size +h2->size;
    HeapNode *N1 = h1->head;
    HeapNode *N2 = h2->head;


    while (N1 && N2)
    {
        //sort according to the degree
        if (N1->degree < N2 ->degree)
        {
            *pos = N1;
            N1 = N1->sibling;
        } else
            {
            *pos = N2;
            N2 = N2->sibling;
        }
        pos = &(*pos) ->sibling;
    }
    if(N1)
        *pos = N1;
    else
        *pos = N2;

    T->head = head;
    return T;

}

//when there is two heap with same degree, link one heap(child) to another heap(root)
static void heap_link(HeapNode *child, HeapNode *root)
{
    //reset the parent and child
    child->parent = root;
    child->sibling = root-> child;
    root->child = child;
    //the degree will +1 after link two heap together
    root->degree++;
}

//In this function, we merge two heaps together and link the heap with the same degree, then return the union heap
BinomialHeap *heap_union(BinomialHeap *h1, BinomialHeap *h2)
{
    BinomialHeap *new_heap = newHeap();
    new_heap->size = h1->size +h2->size;
    new_heap = heap_merge(h1,h2);

    //use prev,x,next to compare the degree and determine whether to link or not
    HeapNode *prev_x , *x , *next_x ;

    if (new_heap==NULL)
        return NULL;

    prev_x = NULL;
    x =  new_heap->head;
    next_x = x->sibling;

    while (next_x != NULL)
    {
        //when current degree equal to next degree or next degree equal to next_next degree
        //keep check the node
        if ((x->degree != next_x->degree) || ((next_x->sibling != NULL) && \
        (next_x->degree == next_x->sibling->degree)))
        {
            prev_x = x;
            x= next_x;
        }
        //current node degree equal to next node and current key smaller than next key,
        // link next node to current node
        else if (x->key <= next_x-> key)
        {
            x->sibling = next_x->sibling;
            heap_link(next_x, x);
        }
        else
        {
            //current node degree equal to next node and current key larger than next key,
            // link current node to next node
            if (prev_x == NULL )
            {
                new_heap->head = next_x;
            }
            else
            {
                prev_x->sibling = next_x;
            }
            heap_link(x,next_x);
            x= next_x;
        }
        next_x = x->sibling;

    }

    return new_heap;
}



// put the time complexity analysis for Insert() : O(logn)
void Insert(BinomialHeap *T, int k, int n, int c, int r, int d)
{ // k: key, n: task name, c: execution time, r: release time, d:deadline 
  // You don't need to check if this task already exists in T
  //setup a new node to a the new heap
  HeapNode *node;
  node = newHeapNode(k,n,c,r,d);
  BinomialHeap *temp = newHeap();
  temp->head = node;
  T->size++;
  T->head = heap_union(T,temp)->head;
  free(temp);
}

//heap reverse is used to isolate node in heap and creat a new heap after deleting node.
static BinomialHeap *heap_reverse(BinomialHeap * heap)
{
    HeapNode *new_head = NULL;
    HeapNode *child = heap->head;
   while (child != NULL)
   {
       //reset the heap 
       HeapNode *next = child->sibling;
       child ->sibling = new_head;
       new_head = child;
       child = next;
   }

    heap->head = new_head;
    return heap;
}


// put your time complexity for RemoveMin() : O(log(n))
//remove the smallest node from the heap and adjust the heap after deleting the node, to keep the heep in order.
HeapNode *RemoveMin(BinomialHeap *T)
{
 // put your code here
 //when deleting the last node in heep
    if (T->size ==1)
    {
        HeapNode *T_head = T->head;
        int key = T_head->key;
        int Taskname = T_head->TaskName;
        int Etime = T_head->Etime;
        int Rtime = T_head->Rtime;
        int Dline = T_head->Dline;

        T->head = NULL;
        T->size--;
        return newHeapNode(key,Taskname,Etime,Rtime,Dline);
    }
    //use prev,x,next to find the smallest node
    HeapNode *smallest = T->head;
    HeapNode *small_prev = NULL;
    HeapNode *small_next = smallest->sibling;
    HeapNode *small_next_prev = smallest;

    while (small_next != NULL)
    {
        //if next smaller than current, keep find next one
        if(small_next ->key <= smallest->key)
        {
            smallest = small_next;
            small_prev = small_next_prev;
        }
        small_next_prev = small_next;
        small_next = small_next->sibling;
    }

    T->size--;
    //return the smallest node by creating a new node
    int k = smallest->key;
    int Task = smallest->TaskName;
    int E = smallest->Etime;
    int R = smallest->Rtime;
    int D = smallest->Dline;
    HeapNode *smallest_node = newHeapNode(k,Task,E,R,D);

    //reset the head if the node(deleted) is the head of the heep
    if (T->head == smallest)
    {
        T->head = smallest->sibling;
    } else{
        small_prev->sibling = smallest->sibling;
    }

    HeapNode *child = smallest->child;
    BinomialHeap *temp = newHeap();
    temp->head = child;
    //reverse the heep before connect to the old heep
    temp = heap_reverse(temp);

    //connect the heap to the T, keep binomialHeap in order
    T->head = heap_union(T,temp)->head;
    free(temp);

    return smallest_node;


}

//In the BinomialHeap, the smallest key always on the head of each child heap
int Min(BinomialHeap *T)
{
    //use min,min_next to compare the smallest node
    HeapNode *min, *min_next;
    min = T->head;
    min_next = min ->sibling;
    while (min_next != NULL)
    {
        if (min_next-> key < min->key)
        {
            min = min_next;
        }
        min_next = min_next ->sibling;
    }
    return min->key;
}

//read the file and convert to the heap.
BinomialHeap *convert2Heap(char *f1)
{
    FILE *file_heap;
    file_heap = fopen(f1,"r");
    char *str = malloc(1000 * sizeof(char));

    BinomialHeap *T = newHeap();
    //check the file is empty or not
    if (file_heap == NULL)
    {
        printf("File 1 does not exist.\n");
        exit(1);
    }
    //set the taskname, Etime, Rtime, Dline to 0
    //counter is used to count the mission current reading
    //number is the totoal number in the file
    //index is used to remember the order of Task, Etime, Rtime, Dline.
    int Taskname = 0, Etime  = 0, Rtime = 0, Dline = 0, counter = 0, index = 0, number = 0;

    while (1)
    {
        //After read the last figure stop while
        if (fscanf(file_heap, "%s", str) == EOF)
            break;
        counter = number/4 +1;
        //use index to test the input one by one.
        switch (index)
        {
            //index = 0 used to check and scanf Taskname
            case 0:
                if (sscanf(str, "%d",&Taskname) != 1)
                {
                    printf("there is input error: Task %d", counter);
                    exit(1);
                } else
                    index++;
                break;
                //index = 1 used to check and scanf Etime
            case 1:
                if (sscanf(str, "%d", &Etime) != 1)
                {
                    printf("there is input error: Task %d", counter);
                    exit(1);
                } else
                    index++;
                break;
                //index = 2 used to check and scanf Rtime
            case 2:
                if (sscanf(str, "%d", &Rtime) != 1)
                {
                    printf("there is input error: Task %d", counter);
                    exit(1);
                } else
                    index++;
                break;
                //index = 3 used to check and scanf Dline
            case 3:
                if (sscanf(str, "%d", &Dline) != 1)
                {
                    printf("there is input error: Task %d", counter);
                    exit(1);
                } else
                    index++;
                break;
        }
        number++;
        //check if collect four figure succeed or not, and insert into heap
        if (index == 4)
        {
            Insert(T, Dline, Taskname, Etime, Rtime, Dline);
            index = 0;
        }
    }
    //check the sun of number is 4k
    if (number % 4 != 0)
    {
        printf("Input Error: Task %d is not enough 4\n",counter);
    }

}
//used to test the heap work
void heap_print(HeapNode* node){
    while (node){
        printf("TaskName is %d\n", node -> TaskName);
        heap_print(node -> child);
        node = node -> sibling;
    }
}

// put your time complexity analysis for MyTaskScheduler here
int TaskScheduler(char *f1, char *f2, int m )
{
 // this part does not work, in order to keep other part work, I delete this part of code.

}

int main() //sample main for testing 
{
    //write this part to test the BinomialHeap is work and function RemoveMin is also work too.
    BinomialHeap * T = newHeap();
    int key[8] = {3,5,23,6,8,1,12,15};
    for (int k = 0; k < 8; k++){
        Insert(T,key[k],k,1,2,3);
    }
    heap_print(T->head);
    printf("---------test-------------");
    RemoveMin(T);
    heap_print(T->head);
    printf("Min is %d\n", Min(T));



//    int i;
//  i=TaskScheduler("samplefile1.txt", "feasibleschedule1.txt", 4);
//  if (i==0) printf("No feasible schedule!\n");
//  /* There is a feasible schedule on 4 cores */
//  i=TaskScheduler("samplefile1.txt", "feasibleschedule2.txt", 3);
//  if (i==0) printf("No feasible schedule!\n");
//  /* There is no feasible schedule on 3 cores */
//  i=TaskScheduler("samplefile2.txt", "feasibleschedule3.txt", 5);
//  if (i==0) printf("No feasible schedule!\n");
//  /* There is a feasible schedule on 5 cores */
//  i=TaskScheduler("samplefile2.txt", "feasibleschedule4.txt", 4);
//  if (i==0) printf("No feasible schedule!\n");
//  /* There is no feasible schedule on 4 cores */
//  i=TaskScheduler("samplefile3.txt", "feasibleschedule5.txt", 2);
//  if (i==0) printf("No feasible schedule!\n");
//  /* There is no feasible schedule on 2 cores */
//  i=TaskScheduler("samplefile4.txt", "feasibleschedule6.txt", 2);
//  if (i==0) printf("No feasible schedule!\n");
//  /* There is a feasible schedule on 2 cores */
 return 0;
}
