# Met Recommendation System

Gabriel Gianordoli and John Choi

MET Media Lab

Spring, 2015

---

Recommendation system based on the examples from Toby Segara's book *Programming Collective Intelligence*.

The data source is a list of items saved by users on their **[MyMet](https://www.metmuseum.org/mymet)** accounts. The files inside **recommendation_item_based** turn the records into a list of similar items, following this sequence:

* **01_make_dict_user_items** groups the records by user: [ { user1: [ item1, item2, ... ], ... } ]
* **02_make_dict_item_users** switches the collection above, grouping items based on the users who saved them: [ { item1: [ user1, user2, ... ], ... } ]
* **03_make_dict_similar_items** runs the similarity algorithms and build a list of 10 similar items for each artwork in the collection: [ { item1: [ similar1, similar2, ..., similar10 ], ... } ]
* **04_json_create** gets more information about each item using [scrapi](http://scrapi.org/). The final format for each item is:


```
{
	item_id: 16584,
	item_title: 'George Washington',
	gallery_number: 140/null, // null if object is not on display
	department: 'egyptian art'/null,
	img_url_web: 'http://...', // null if it doesn't have image?
	img_url_big: 'http://...', // null if it doesn't have image?
	similar_items: [
			{ item_id: 004327, similarity: 0.01 },
			{ item_id: 052345, similarity: 0.005 },
			...
	]
}
```

See more at the project description on the [MET Media Lab's Hackpad](https://metmedialab.hackpad.com/Serendipity-2k4a1OyAH3D)