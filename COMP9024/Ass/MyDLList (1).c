// Author: ZANNING WANG
// Student ID: z5224151
// Platform: Windows
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <stdbool.h>
#include <string.h>

// all the basic data structures and functions are included in this template
// you can add your own auxiliary functions as you like 

// data structures representing DLList

// data type for nodes
typedef struct DLListNode {
	int  value;  // value (int) of this list item 
	struct DLListNode *prev;
	// pointer previous node in list
	struct DLListNode *next;
	// pointer to next node in list
} DLListNode;

//data type for doubly linked lists
typedef struct DLList{
	int  size;      // count of items in list
	DLListNode *first; // first node in list
	DLListNode *last;  // last node in list
} DLList;

// create a new DLListNode
DLListNode *newDLListNode(int it)
{
	DLListNode *new;
	new = malloc(sizeof(DLListNode));
	assert(new != NULL);
	new->value = it;
	new->prev = new->next = NULL;
	return new;
}

// create a new empty DLList
DLList *newDLList()
{
	DLList *L;

	L = malloc(sizeof (struct DLList));
	assert (L != NULL);
	L->size = 0;
	L->first = NULL;
	L->last = NULL;
	return L;
}
//creat a new function to insert node to the bottom of the list.
DLList *insertnode (struct DLList *oldlist ,int val)
        {
    if (oldlist == NULL) return newDLList();
    if (oldlist->first == NULL)
    {
        oldlist->first = newDLListNode(val);
        oldlist->last = oldlist->first;
    } else
        {
        DLListNode *temp = oldlist->last; //save the node before link the new node.
        DLListNode *new_node = newDLListNode(val);
        oldlist->last = new_node;//link the last node to the list
        temp->next = new_node;
        new_node->prev = temp;

    }
            return oldlist;
        }

//creat a new funtion to check given value if it is exist in the new_list
bool checkexist(DLListNode *first_node, int val)
{
    if (first_node ==NULL) return false;
    if (first_node->value ==val)
    {
        return true;
    } else{
        return checkexist(first_node->next,val);
    }
}


// create a DLList from a text file
// put your time complexity analysis for CreateDLListFromFileDlist() o(n)
DLList *CreateDLListFromFileDlist(const char *filename) {
    // put your code here
    char input[128];
    int val;
    FILE *f;
    DLList *newlist = newDLList();
    f = fopen(filename, "r");

    if (strcmp(filename, "stdin") != 0) {
        if (f == NULL)
        {
            fprintf(stderr, "fail to open the file.");
        }
    } else {
        //manual input
        f = stdin;
    }
    while (fscanf(f, "%s", input) != EOF) {
        if (f == stdin && strcmp(input, "end") == 0) {
            return newlist;
        } else{
            fprintf(stderr, "Invalid input!");
        }
        val = atoi(input);
        newlist = insertnode(newlist, val);

    }

    fclose(f);
    return newlist;
}
// clone a DLList
// put your time complexity analysis for cloneList() O(n)
DLList *cloneList(DLList *u)
{
 // put your code here
    if(u==NULL)
    {
        return NULL;
    }
    if (u->first == NULL)//create the list from function
        return newDLList();
    DLList *clone_list = newDLList();
    DLListNode *temp = u->first;
    while (temp!=NULL)//insertnode until the last node trans to null
    {
        insertnode(clone_list,temp->value);
        temp = temp->next;
    }
    return clone_list;
}



// compute the union of two DLLists u and v
// put your time complexity analysis for O(n^2)
//In this function, there is a function Insertnode, which time complexity is O(n), therefore the whole
//function time complexity is O(n^2).
DLList *setUnion(DLList *u, DLList *v)
{
 // put your code here
	DLList *Unionlist = cloneList(u);
	if (u == NULL || u->first == NULL)
		return v;
	if (v == NULL || v->first == NULL)
		return newDLList();

	DLListNode *temp_v = v->first;

	while (temp_v !=NULL){
	    if (!checkexist(u->first,temp_v->value))//check the node_v whether in list_u or not
        {
	        insertnode(Unionlist,temp_v->value);
        }
	    temp_v = temp_v->next;//check next node in list_v
	}

	return Unionlist;
	
}

// compute the insection of two DLLists u and v
// time complexity analysis for intersection() is O(n^2)(in this function there is a function insertnode
//which time complexity is O(n));
DLList *setIntersection(DLList *u, DLList *v)
{
	DLList *Interlist = newDLList();
	if (u==NULL || v ==NULL)
        return NULL;
	DLListNode *temp_u = u->first;
	while (temp_u != NULL){
	    if (checkexist(v->first,temp_u->value)){//check node_u if in list_v
	        insertnode(Interlist,temp_u->value);
	    }
	    temp_u = temp_u->next;
	}

	return Interlist;
}

// free up all space associated with list
// time complexity O(n)
void freeDLList(DLList *L)
{
	DLListNode *first = L->first;
    DLListNode *temp = first ->next;
	while (temp != NULL)
	{
		free(first);
		first = temp;
		temp = temp->next;
	}
	free(L);
		
}


// display items of a DLList
// put your time complexity analysis for printDDList(): O(n)
void printDLList(DLList *u)
{
 // put your code here
	if(u==NULL){
		printf("empty\n");
		return;
	}

	DLListNode* temp = u->first;
	while (temp != NULL)
	{
		printf("%d\n",temp->value);
		temp = temp->next;
	}
	 
}

int main()
{
 DLList *list1, *list2, *list3, *list4;

 list1=CreateDLListFromFileDlist("File1.txt");
 printDLList(list1);

 list2=CreateDLListFromFileDlist("File2.txt");
 printDLList(list2);

 list3=setUnion(list1, list2);
 printDLList(list3);

 list4=setIntersection(list1, list2);
 printDLList(list4);

 freeDLList(list1);
 freeDLList(list2);
 freeDLList(list3);
 freeDLList(list4);

    printf("-------------------------test-line5--------------------------\n");
 printf("please type all the integers of list1\n");
 list1=CreateDLListFromFileDlist("stdin");

    printf("--------------------------6--------------------------\n");
 printf("please type all the integers of list2\n");
 list2=CreateDLListFromFileDlist("stdin");

 list3=cloneList(list1);
 printDLList(list3);
 list4=cloneList(list2);
 printDLList(list4);

 freeDLList(list1);
 freeDLList(list2);
 freeDLList(list3);
 freeDLList(list4);

 return 0; 
}
