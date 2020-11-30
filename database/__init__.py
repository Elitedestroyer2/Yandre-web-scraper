class DbManager(object):

    from ._databaseConnection import create_connection, close_connection
    from ._addedCharacterTable import (check_added_character_exsits, enter_added_new_character,
                                            update_added_character_amount, get_added_characters_names,
                                            get_added_entry, get_added_characters_table, 
                                            delete_added_character, delete_added_table, 
                                            create_added_table, 
                                            get_added_characters_table_first_name, 
                                            check_added_characters_table_count)
    from ._suggestionsTable import (delete_suggestions_table, create_suggestions_table, 
                                            added_character_to_suggest_list, search_for_suggestions,
                                            grab_suggestion_list)
    from ._charactersTable import (check_character_exsits, enter_new_character, update_character_amount, 
                                            get_characters_names, delete_character, get_character_table, delete_table, 
                                            create_table)

