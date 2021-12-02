#!/usr/bin/env python
from datetime import datetime
import pickle
import os
import time
import subprocess
import sys

today = datetime.now()
todays_date = today.strftime("%d_%m_%Y")
home_dir = os.path.expanduser('~')
master_list_location = f'{home_dir}/.pickles/refs.pkl'
todays_list_location = f"{home_dir}/.pickles/{todays_date}_refs.pkl"


class OtherMethods:
    @staticmethod
    def attempt_to_copy(choice):
        """
        Attempt to copy to clipboard, if pyperclip isn't installed give the option to install it automatically
        or manually
        :param choice:
        :return:
        """
        copy_list = PickleFunctions.retrieve_recent_list()
        # copy_this = ""
        ref, cite = copy_list[-1]
        if choice == "reference":
            copy_this = ref
        elif choice == "citation":
            copy_this = cite
        elif choice == "both":
            copy_this = f"{ref} {cite}"
        else:
            sorted_copy_list = sorted(copy_list)
            copy_this = ""
            for ref, cite in sorted_copy_list:
                copy_this += f"{ref} {cite}\n"

        while True:
            try:
                import pyperclip
                # print(copy_this)
                pyperclip.copy(copy_this)
                print("\nCopied...")
                time.sleep(1)
                break

            except ImportError:
                install_now = input("to add this functionality install pyperclip using: \n pip install pyperclip\n\n  "
                                    "or\n\n-Install now? Press 'i'"
                                    "\n-Not now  (any other key)\n")
                if install_now[0].lower() == "i":
                    OtherMethods.install("pyperclip")
                else:
                    break

    @staticmethod
    def install(package):
        """
        Install pyperclip, if instructed to do so, so that a user can copy to the clipboard
        :param package:
        :return:
        """
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    @staticmethod
    def create_a_reference():
        """
        Accepts user input to help build a reference and citation, which is then copied to the clipboard so it
        can be added where required
        :return: (str) reference and citation
        """

        first_names = input("Please enter the author's first name(s): ")
        if first_names == "":
            first_names = None
            authors_initials = ""
        else:
            first_names = first_names.strip()
            author_first_names = [name.capitalize() for name in first_names.split(' ')]
            authors_initials = ""
            for f_name in author_first_names:
                authors_initials += f"{f_name[0]}."
        author_last_name = input("Last name: ")
        article_year = input("Article year: ")
        article_title = input("Article title: ")
        publisher = input("Publisher: ")
        website_url = input("URL: ")
        accessed_date = input("Accessed date: ")

        my_new_reference = Reference(author_fname=authors_initials, author_lname=author_last_name,
                                     article_year=article_year, article_title=article_title, publisher=publisher,
                                     website_url=website_url, accessed_date=accessed_date)

        reference = my_new_reference.create_reference(my_new_reference)
        citation = my_new_reference.create_citation(my_new_reference)

        return reference, citation


class PickleFunctions:
    @staticmethod
    def persistence(list_to_save, location):
        """
        Save references to pickle list
        :param location:
        :param list_to_save:
        :return:
        """
        # PickleFunctions.create_empty_list()
        open_file = open(location, "wb")
        pickle.dump(list_to_save, open_file)
        open_file.close()

    @staticmethod
    def create_empty_list(list_to_create):
        """
        Create empty list
        :return:
        """
        refs_list = []
        open_file = open(list_to_create, "wb")
        pickle.dump(refs_list, open_file)
        open_file.close()

    @staticmethod
    def create_empty_list_if_none_exists(create_location):
        """
        Create an empty list if no list exists
        :return:
        """
        if os.path.exists(create_location):
            pass
        else:
            PickleFunctions.create_empty_list(create_location)

    @staticmethod
    def retrieve_recent_list():
        """
        Get the most up to date list of references
        :return:
            :argument1 list (loaded_list)
        """
        open_file = open(todays_list_location, "rb")
        loaded_list = pickle.load(open_file)
        open_file.close()
        # print(f"todays_list_location: {todays_list_location}")
        return loaded_list

    @staticmethod
    def retrieve_complete_list():
        """
        Get the most up to date list of references
        :return:
            :argument1 list (loaded_list)
        """
        open_file = open(master_list_location, "rb")
        loaded_list = pickle.load(open_file)
        open_file.close()
        return loaded_list


class Reference:
    def __init__(self, author_fname, author_lname, article_year, article_title, publisher, website_url, accessed_date):
        self.author_fname = author_fname
        self.author_lname = author_lname
        self.article_year = article_year
        self.article_title = article_title
        self.publisher = publisher
        self.website_url = website_url
        self.accessed_date = accessed_date

    @staticmethod
    def create_reference(self):
        # TODO - Add book referencing output
        if self.author_fname == "" or self.author_fname is None:
            return f"{self.author_lname} ({self.article_year}). '{self.article_title}', " \
                   f"{self.publisher}, Available: {self.website_url} [Last accessed {self.accessed_date}]."
        else:
            return f"{self.author_lname}, {self.author_fname} ({self.article_year}). '{self.article_title}', " \
                   f"{self.publisher}, Available: {self.website_url} [Last accessed {self.accessed_date}]."

    @staticmethod
    def create_citation(self):
        if self.author_lname == "" or self.author_lname is None:
            # print("blank or null last name")
            return f"({self.article_title}, {self.article_year})"
        else:
            return f"({self.author_lname}, {self.article_year})"


class Menu:
    # my_list = PickleFunctions.retrieve_updated_list()
    @staticmethod
    def print_menu():
        """
        Print the menu, accept user input and complete the desired tasks
        :return:
        """
        while True:
            choice = input("\nMenu"
                           "\n1. Create new web citation and link?"
                           "\n2. Create new text citation and link?"
                           "\n3. Display recent citations?"
                           "\n4. Display all citations?"
                           "\n5. Delete previous citations?"
                           "\n6. Copy last reference to clipboard?"
                           "\n7. Copy last citation to clipboard?"
                           "\n8. Copy reference and citation to clipboard?"
                           "\n9. Copy all today's citations to clipboard?"
                           "\nX. Exit\n\n")

            if choice == "1":
                Menu.create_citation_and_store()
            
            elif choice == "2":
                # Menu.create_citation_and_store()
                print("\nFeature coming soon...")
                time.sleep(2)

            elif choice == "3":
                Menu.display_recent_citations()

            elif choice == "4":
                Menu.display_all_citations()

            elif choice == "5":
                Menu.delete_all_citations()

            elif choice == "6":
                Menu.copy_options("reference")

            elif choice == "7":
                Menu.copy_options("citation")

            elif choice == "8":
                Menu.copy_options("both")

            elif choice == "9":
                Menu.copy_options("all")

            elif choice.lower() == "x":
                Menu.exit()

            else:
                print("Check your input!\n")
                time.sleep(2)

    @staticmethod
    def create_citation_and_store():
        """
        Menu item 1: create new citation
        :return:
        """
        my_ref, my_cite = OtherMethods.create_a_reference()
        complete_list = PickleFunctions.retrieve_complete_list()
        todays_list = PickleFunctions.retrieve_recent_list()
        ref_and_cite = (my_ref, my_cite)
        complete_list.append(ref_and_cite)
        todays_list.append(ref_and_cite)
        PickleFunctions.persistence(complete_list, master_list_location)
        PickleFunctions.persistence(todays_list, todays_list_location)
        print(f"\n{my_ref}")
        OtherMethods.attempt_to_copy("both")
        time.sleep(1)

    @staticmethod
    def display_recent_citations():
        """
        Menu item 2: display all citations in memory
        :return:
        """
        display_list = PickleFunctions.retrieve_recent_list()
        if len(display_list) == 0:
            print("\nNothing to display...\n")
            time.sleep(1)
        else:
            print("")
            for ref, cite in display_list:
                print(f"{ref} {cite}")
            time.sleep(3)

    @staticmethod
    def display_all_citations():
        """
        Menu item 2: display all citations in memory
        :return:
        """
        display_list = PickleFunctions.retrieve_complete_list()
        if len(display_list) == 0:
            print("\nNothing to display...\n")
            time.sleep(1)
        else:
            print("")
            for ref, cite in display_list:
                print(f"{ref} {cite}")
            time.sleep(3)

    @staticmethod
    def delete_all_citations():
        """
        Menu item 3: delete all citations that exist in memory
        :return:
        """
        final_check = input("Sure? (y / any other key)\n")
        if final_check.lower() == "y":
            PickleFunctions.create_empty_list(master_list_location)
            print("Deleted")
            time.sleep(1)
        else:
            print("Taking you back to the menu...")
            time.sleep(1)

    @staticmethod
    def copy_options(choice_made):
        """
        Menu item 4: copy last reference to the clipboard.  Give option to install pyperclip if necessary
        :param choice_made:
        :return:
        """
        OtherMethods.attempt_to_copy(choice_made)

    @staticmethod
    def exit():
        """
        Exit program
        :return:
        """
        print("Goodbye")
        time.sleep(2)
        exit(0)


def main():
    """
    Main function:
        Create an empty master list if this is the first time the program is running,
        and also a pickle list for today.  Print the menu so the user can make their choices
    :return:
    """
    PickleFunctions.create_empty_list_if_none_exists(master_list_location)
    PickleFunctions.create_empty_list_if_none_exists(todays_list_location)
    Menu.print_menu()


if __name__ == '__main__':
    main()
