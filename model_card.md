# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---TuneTailor 1.0

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---This system recommends a handful of songe from a small, predefined catalog. It makes these suggestions by matching song attributes to a user's explicitly stated preferences for genre, mood, energy, and acoustic sound. This model is designed purely for educational and simulation purposes to demonstrate the core concepts of a content-based recommender; it is not intended for real-world application with actual users.

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---This recommender works by scoring every song in its catalog against a user's taste profile to find the best matches
- It looks at four main features of a song: its genre (like 'pop' or 'rock'), its mood (like 'happy' or 'chill'), its energy level, and its acousticness (how much of the track is non-electric).
-  It uses a simple "taste profile" that stores the user's favorite genre, favorite mood, a target energy level they're looking for, and whether or not they like acoustic music.
- The system compares a song's features to the user's profile and awards points. A match in genre is worth the most points, followed by a mood match. It also awards points if a song's energy is very close to the user's target, and for how well its acoustic level matches the user's preference. These points are added up to create a final "similarity score" for the song. The higher the score, the better the recommendation.

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---There are 27 songs in the songs.csv dataset. With the help of Copilot, I added 17 out of the 27 songs. The dataset is diverse and includes a mix of electronic and acousticc, mainstream niche genres such as pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, reggae, country, classical, etc. The moods that are represented are happy, chill, intense, relaxed, moody, focused, energetic, uplifting, sad, peaceful, epic, thoughtful, nostalgic, etc. The dataset does not reflect a single person's taste. It is a curated collection designed for testing a recommender system.

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---My recommender can explain exactly why it chose a particular song. The recommendations are a direct and istant reflection of the user's stated preferences. The design is easy to understand since the entire logic is contained in a few functions , which is eficient for small-to-medium sized catalog of songs. It worked well with the default user profile which included pop as the genre and happy as the mood. 

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---The recommender is stateless. It cannot learn from a user's past interactions. Also, it is purely content-based system, so it will only recommend songs that are similar to what the user already likes. It will struggle to introduce the user to completely new and different genres or artist they might enjoy. The UserProfile simplifies human taste significantly.In addition, the recommenders world is limited to the songs listed in the songs.csv file. The weights I defined in the score_song function are based my own assumptions about what makes a good recommendation. Unrecognized genres or moods provide low scores for recommendations.

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---I ran the simple default user prifile with the genre being pop and the mood being happy. The system behaved according to what I was expecting. I was surprised that changeing the weight of the genre attribute did not change that scores all that much. 

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---I would definitly add more ways to handle complex user tastes. I would add a considerate amount of more songs to the songs.csv file. I would test for correct user input type.

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned about the difference between collaborative and content-based filtering and how many larger streaming companies utilize a mixture of both techniques to recommend similar and new music to listeners. It is really interesting to me what goes on behind the logic of those recommendations. Bias could show up in the system in the form of the dataset itself or algorithmic bias. Although, my dataset is diverse, it is small, as a result a user that likes one of those genres will get very few, if any , recommendations. The initial 10 songs were heavily focused on modern electronic-influenced genres like pop, lofi, and synthwave. If I hadn't added more variety, the system would have a strong bias towards this type of music, creating a "filter bubble" where users are never exposed to anything else. The concepts of energy or mood might be interpreted differently across cultures. A song considered "happy" in one culture might be perceived differently in another. In my first version score_song function, I assigned genre a weight of 0.5. This means a genre match is considered overwhelmingly important. This creates a bias where the system will almost always favor a song of the correct genre, even if its other attributes are a poor match. While my system doesn't explicitly track popularity, real-world systems often do. They tend to recommend what is already popular, creating a feedback loop where popular artists get more popular, and emerging artists are ignored.
