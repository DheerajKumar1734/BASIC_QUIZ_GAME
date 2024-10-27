
def count_words(text):
    """
    This function counts the number of words in the input text.
    It splits the text by spaces and filters out any empty strings.
    """
    # Now we Split the text into words using spaces as delimiters
    words = text.split()
    
    # Return the count of words
    return len(words)

def main():
    """
    Main function to interact with the user and display the word count.
    """
    # We have to enter a sentence or paragraph
    user_input = input("Enter a sentence or paragraph: ").strip()

    # We can check if there are any errors using the Error Handling: Check if input is empty
    if not user_input:
        print("Error: You entered an empty input. Please try again.")
        return

    # We now Call the count_words function to count the words
    word_count = count_words(user_input)

    # Finally, it display's the word count to the user through the console
    print(f"Word Count: {word_count}")

if __name__ == "__main__":
    main()