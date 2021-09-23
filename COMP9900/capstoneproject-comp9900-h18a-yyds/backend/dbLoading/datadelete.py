from util.database import *
from util.helpers import *
from configs.collection_names import *

db = DB()

superVs = [ 'eb35b81adafd11eb892559354efcec79',
            '31f9a248dafe11eb892559354efcec79', 
            '4f31261adafe11eb892559354efcec79',
            '81a431bedafe11eb892559354efcec79',
            '9f0cf330dafe11eb892559354efcec79',
            'e1c10018dafe11eb892559354efcec79',
            'f014d838dafe11eb892559354efcec79',
            '0010aba4daff11eb892559354efcec79',
            '17f78c60daff11eb892559354efcec79',
            '609a46ecdaff11eb892559354efcec79']

total = 0
for uid in superVs:
    rids = db.get_one_from_collection(USER_RECIPES, 'user_id', uid)['recipe_list']

    print('user:', uid, ', post_n: ', len(rids), '\n******************\n')
    total += len(rids)
    for r in rids:
        rid = r['recipe_id']
        # print(rid,'\n')
        db.delete_one_from_collection(RECIPES, '_id', rid)
        
        db.pop_from_nested_array(USER_RECIPES, 'recipe_list', 'user_id', uid, recipe_id=rid)
        
        db.update_fields_values(USERS, '_id', uid, recipe_num=-1)
print('\ntotal post : ', total)