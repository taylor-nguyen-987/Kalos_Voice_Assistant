import enchant
from nltk.corpus import stopwords
from nltk import word_tokenize
import json

class Response:

    def get_response(self, text):

        """Returns a response in string format"""

        myjfile = open('pokemon.json')
        jsondata = myjfile.read()
        myjfile.close()

        object = json.loads(jsondata)
        
        boolean = False #checks whether the text contains a Pokemon name
        name, info = "", ""
        for word in text:
            if (object["pokemons"]).get(word) is not None:
                """if a Pokemon name exists in the string, retrieve its information"""
                info = (object["pokemons"])[word]
                name = word #Store the Pokemon's name
                boolean = True
                break
        if boolean is True:
            response = name

            #POKEMON TYPINGS
            typings = ", ".join(info[1])
            response = f"{response.capitalize()} is a {typings} Pokemon."

            #STATS
            response = f"{response} It has {(info[2])[0]} HP, {(info[2])[1]} attack points, {(info[2])[2]} defense points, and {(info[2])[5]} speed points."
            response = f"{response} It also has {(info[2])[3]} points for its special attack and {(info[2])[4]} points for its special defense."
            
            #TRAINERS
            if (len(info[3][0])>0): #Nonempty
                response = f"{response} {(info[3][0])[0]} from {(info[3][0])[1]} trained this Pokemon."
            
            #WHEREABOUTS
            if (len(info[4])>0): #Location in Pokemon X
                locations = ", ".join(info[4][0])
                response = f"{response} It can be found in {locations} in Pokemon X."
            
            #ORIGIN
            response = f"{response} Lastly, it is from {(info[5])}."
            return response
        else:
            return "Pokemon cannot be identified."
            
class SpellChecker:

    """Corrects the voice input if needed"""
    #TODO: POST EDITING STRINGS

    def correct(self, string):
        #Identifies keys words in the phrase and gets the name of the pokemon the user is trying to ask about

        #Normalize the string
        string = string.lower() #lowercase string
        clean_input = " ".join([word for word in string.split() if word not in stopwords.words('english')]) #remove stopwords

        poke_dict = enchant.PyPWL("pokemon_names.txt")
        
        #Tokenization
        tokens = word_tokenize(clean_input)
        print(tokens)