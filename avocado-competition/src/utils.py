def create_map_one_to_many(df, col_one, col_many):
    """This function creates a dictionary that maps one key to many values

    Args:
        df (dataframe): dataframe to use for the mapping
        col_one (string): column to use for the keys
        col_many (string): column to use for the values

    Returns:
        dictionary.
    """
    #create a dictionary of sums - winners to catch multiple winners
    my_dict = {}

    for one, many in zip(df[col_one].tolist(), df[col_many].tolist()):
        if one in my_dict.keys():
            my_dict[one].append(many)
        else:
            my_dict[one] = [many]
    
    return my_dict
