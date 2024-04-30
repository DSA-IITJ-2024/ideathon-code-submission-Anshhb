#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CATEGORIES 11
#define MAX_KEYWORDS_PER_CATEGORY 10
#define HASH_TABLE_SIZE 50

// Structure to represent a transaction
typedef struct {
    char date[20];
    float amount;
    char vendor[50];
    char description[100];
    char category[50];
    char item[50]; // New field to track the item
} Transaction;


// Structure for Binary Search Tree node
typedef struct TreeNode {
    Transaction transaction;
    struct TreeNode* left;
    struct TreeNode* right;
} TreeNode;

// Structure to represent budget for a category
typedef struct {
    char category[50];
    float amount;
} Budget;

// Predefined categories and their keywords
typedef struct {
    char name[50];
    char keywords[MAX_KEYWORDS_PER_CATEGORY][50];
    int numKeywords;
} Category;

// Function prototypes
TreeNode* createNode(Transaction* transaction);
TreeNode* insertTransaction(TreeNode* root, Transaction* transaction);
void printTransactions(TreeNode* root);
char* recommendCategory(char* description);
void addExpense(TreeNode** root);
TreeNode* deleteTransaction(TreeNode* root, char* date);
void editExpense(TreeNode** root);
void deleteExpense(TreeNode** root);
void setBudget(Budget* budgets, int* numBudgets);
void trackSpending(TreeNode* root, Budget* budgets, int numBudgets);
void calculateSpending(TreeNode* root, float* totalSpending);

// Predefined categories and their keywords
Category categories[MAX_CATEGORIES] = {
    {"Food", {"grocery", "restaurant", "dining", "food"}, 4},
    {"Rent", {"rent", "housing", "apartment"}, 3},
    {"Clothes", {"clothes", "shoes", "jewelry"}, 3},
    {"Entertainment", {"entertainment", "movies", "music", "cinema", "music"}, 5},
    {"Travel", {"travel", "flight", "hotel", "rental"}, 4},
    {"Miscellaneous", {"miscellaneous", "gift", "purchases", "subscriptions"}, 4},
    {"Pet", {"pet", "dog", "cat"}, 3},
    {"Health", {"health", "medical", "insurance", "pharmacy", "drug", "prescription"}, 6},
    {"Education", {"education", "school", "college", "university"}, 4},
    {"Electronics", {"electronics", "computer", "laptop", "phone", "tablet"}, 5},
    {"Home", {"home", "furnishings", "kitchen", "bathroom", "bedroom", "bathroom", "laundry"}, 6},
    // Add more categories and their keywords as needed
};

#define NUM_CATEGORIES sizeof(categories) / sizeof(categories[0])


// Function to create a new BST node
TreeNode* createNode(Transaction* transaction) {
    TreeNode* newNode = (TreeNode*)malloc(sizeof(TreeNode));
    if (newNode != NULL) {
        newNode->transaction = *transaction;
        newNode->left = NULL;
        newNode->right = NULL;
    }
    return newNode;
}

// Function to insert transaction into BST
TreeNode* insertTransaction(TreeNode* root, Transaction* transaction) {
    if (root == NULL) {
        return createNode(transaction);
    }
    // Compare transaction dates to decide left or right subtree
    if (strcmp(transaction->date, root->transaction.date) < 0) {
        root->left = insertTransaction(root->left, transaction);
    } else {
        root->right = insertTransaction(root->right, transaction);
    }
    return root;
}


void printTransactions(TreeNode* root) {
    if (root != NULL) {
        printTransactions(root->left);
        printf("Date: %s, Amount: %.2f, Vendor: %s, Description: %s, Category: %s, Item: %s\n",
            root->transaction.date, root->transaction.amount,
            root->transaction.vendor, root->transaction.description,
            root->transaction.category, root->transaction.item); // Updated print statement
        printTransactions(root->right);
    }
}


// Function to recommend a category based on transaction description
char* recommendCategory(char* description) {
    // Iterate through predefined categories
    for (int i = 0; i < NUM_CATEGORIES; i++) {
        // Iterate through keywords of each category
        for (int j = 0; j < categories[i].numKeywords; j++) {
            // Check if the keyword is present in the description
            if (strstr(description, categories[i].keywords[j]) != NULL) {
                // If a match is found, return the category name
                return categories[i].name;
            }
        }
    }
    // If no match is found, return a default category
    return "Other";
}

void addExpense(TreeNode** root) {
    Transaction newTransaction;
    printf("Enter transaction details:\n");
    printf("Date (YYYY-MM-DD): ");
    scanf("%s", newTransaction.date);
    printf("Amount: ");
    scanf("%f", &newTransaction.amount);
    printf("Vendor: ");
    scanf("%s", newTransaction.vendor);

    // Display category options for the user to choose from
    printf("Select expense category:\n");
    for (int i = 0; i < NUM_CATEGORIES; i++) {
        printf("%d. %s\n", i + 1, categories[i].name);
    }
    int categoryChoice;
    printf("Enter category choice: ");
    scanf("%d", &categoryChoice);

    // Validate category choice
    if (categoryChoice < 1 || categoryChoice > NUM_CATEGORIES) {
        printf("Invalid category choice.\n");
        return;
    }

    // Copy the selected category to the new transaction
    strcpy(newTransaction.category, categories[categoryChoice - 1].name);

    // Display subcategory options for the selected category
    printf("Select expense subcategory:\n");
    for (int i = 0; i < categories[categoryChoice - 1].numKeywords; i++) {
        printf("%d. %s\n", i + 1, categories[categoryChoice - 1].keywords[i]);
    }
    int subcategoryChoice;
    printf("Enter subcategory choice: ");
    scanf("%d", &subcategoryChoice);

    // Validate subcategory choice
    if (subcategoryChoice < 1 || subcategoryChoice > categories[categoryChoice - 1].numKeywords) {
        printf("Invalid subcategory choice.\n");
        return;
    }

    // Copy the selected subcategory to the new transaction
    strcpy(newTransaction.description, categories[categoryChoice - 1].keywords[subcategoryChoice - 1]);

    printf("Item: ");
    scanf("%s", newTransaction.item); // Added input for item

    *root = insertTransaction(*root, &newTransaction);
    printf("Expense added successfully!\n");
}






void editExpense(TreeNode** root) {
    char item[50]; // Input variable for item
    printf("Enter the item of the expense to edit: ");
    scanf("%s", item);

    TreeNode* current = *root;
    TreeNode* parent = NULL;

    // Search for the node to edit based on the item
    while (current != NULL) {
        if (strcmp(item, current->transaction.item) == 0) {
            break;
        }
        parent = current;
        if (strcmp(item, current->transaction.item) < 0) {
            current = current->left;
        } else {
            current = current->right;
        }
    }

    // If node found
    if (current != NULL) {
        printf("Enter updated transaction details:\n");
        printf("Amount: ");
        scanf("%f", &current->transaction.amount);
        printf("Vendor: ");
        scanf("%s", current->transaction.vendor);
        printf("Description: ");
        scanf(" %[^\n]s", current->transaction.description);
        printf("Category: ");
        scanf("%s", current->transaction.category);
        printf("Item: ");
        scanf("%s", current->transaction.item); // Allow changing the item name
        printf("Expense updated successfully!\n");
    } else {
        printf("Expense with item %s not found.\n", item);
    }
}

TreeNode* deleteTransactionByItem(TreeNode* root, char* item) {
    if (root == NULL) {
        return root;
    }
    if (strcmp(item, root->transaction.item) < 0) {
        root->left = deleteTransactionByItem(root->left, item);
    } else if (strcmp(item, root->transaction.item) > 0) {
        root->right = deleteTransactionByItem(root->right, item);
    } else {
        // Node with only one child or no child
        if (root->left == NULL) {
            TreeNode* temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            TreeNode* temp = root->left;
            free(root);
            return temp;
        }
        // Node with two children: Get the inorder successor (smallest in the right subtree)
        TreeNode* temp = root->right;
        while (temp->left != NULL) {
            temp = temp->left;
        }
        // Copy the inorder successor's content to this node
        root->transaction = temp->transaction;
        // Delete the inorder successor
        root->right = deleteTransactionByItem(root->right, temp->transaction.item);
    }
    return root;
}



void deleteExpense(TreeNode** root) {
    char item[50]; // Input variable for item
    printf("Enter the item of the expense to delete: ");
    scanf("%s", item);

    *root = deleteTransactionByItem(*root, item); // Call the modified deleteTransactionByItem function
    printf("Expense deleted successfully!\n");
}


void setBudget(Budget* budgets, int* numBudgets) {
    printf("Enter the number of budget categories: ");
    scanf("%d", numBudgets);
    for (int i = 0; i < *numBudgets; i++) {
        printf("Enter category name: ");
        scanf("%s", budgets[i].category);
        printf("Enter budget amount for %s: ", budgets[i].category);
        scanf("%f", &budgets[i].amount);
    }
}

// Function to track spending against budgets
void trackSpending(TreeNode* root, Budget* budgets, int numBudgets) {
    // Initialize total spending for each category to 0
    float totalSpending[MAX_CATEGORIES] = {0};

    // Traverse the BST to calculate spending for each category
    calculateSpending(root,totalSpending);
    // Display spending and compare with budgets
    printf("Category\tBudget\t\tSpending\tStatus\n");
    for (int i = 0; i < numBudgets; i++) {
        printf("%s\t\t%.2f\t\t%.2f\t\t%s\n", budgets[i].category, budgets[i].amount,totalSpending[i], (totalSpending[i] <= budgets[i].amount) ? "Under Budget" : "Over Budget");
    }
}
// Helper function to recursively calculate spending for each category
void calculateSpending(TreeNode* root, float* totalSpending) {
    if (root != NULL) {
        for (int i = 0; i < NUM_CATEGORIES; i++) {
            if (strcmp(root->transaction.category, categories[i].name) == 0) {
                totalSpending[i] += root->transaction.amount;
                break;
            }
        }
        calculateSpending(root->left, totalSpending);
        calculateSpending(root->right, totalSpending);
    }
}
// Main function
int main() {
    TreeNode* root = NULL;
    Budget budgets[MAX_CATEGORIES];
    int choice;
    int numBudgets = 0; // Initialize numBudgets to 0

    do {
        printf("\nExpense Tracker Menu:\n");
        printf("1. Add Expense\n");
        printf("2. Edit Expense\n");
        printf("3. Delete Expense\n");
        printf("4. View Expenses\n");
        printf("5. Set Budget\n");
        printf("6. Track Spending\n");
        printf("7. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                addExpense(&root);
                break;
            case 2:
                editExpense(&root);
                break;
            case 3:
                deleteExpense(&root);
                break;
            case 4:
                printf("\nAll Transactions:\n");
                printTransactions(root);
                break;
            case 5:
                setBudget(budgets, &numBudgets); // Pass the address of numBudgets
                break;
            case 6:
                trackSpending(root, budgets, numBudgets);
                break;
            case 7:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 7);

    return 0;
}