from embeddings.mongodb_client import create_journal_entry, create_product_entry
from embeddings.mongodb_client import journal_entries_col, products_col  # import collections
from embeddings.vector_store import show_all_entries

def main():
    # Create a sample journal entry and get the returned document (with _id)
    habit = create_journal_entry("user123", "Had coffee this morning and felt great!")
    
    # Pass the habit _id to link the product
    create_product_entry("user123", "Coffee Beans", "Beverage", linked_habit_id=habit["_id"])

    #dummy    
    # Show all entries stored in ChromaDB, now linked
    show_all_entries()

    # Print raw MongoDB entries for debugging
    print("\n=== MongoDB Journal Entries ===")
    for doc in journal_entries_col.find({"user_id": "user123"}):
        print(doc)
    
    print("\n=== MongoDB Product Entries ===")
    for doc in products_col.find({"user_id": "user123"}):
        print(doc)

if __name__ == "__main__":
    main()
