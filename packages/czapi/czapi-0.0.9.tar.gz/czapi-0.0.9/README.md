# Welcome to czapi
> A basic API for scraping curling boxscores off of the popular <a href='https://www.curlingzone.com'>CurlingZone</a> website. 


## Install

```
pip install czapi
```

## How to use

```python
import czapi.api as api
```

## General Information
The czapi is based around the `LinescorePage` object which represents a linescore page, shown below:

![Linescore Page](nbs\imgs\game_by_event_draw_game_number.png)

Creating an instance of the `LinescorePage` class gives access to every boxscore on that linescore page.

```python
linescore_page = api.LinescorePage(cz_event_id = 6400, cz_draw_id = 2)
```

The boxscores on the linescore page can be accessed through the `boxscores` property which returns a list of boxscores.

```python
linescore_page.boxscores
```




    [defaultdict(list,
                 {'Wayne Tuck Jr.': defaultdict(list,
                              {'href': 'event.php?view=Team&eventid=6400&teamid=144353&profileid=12486#1',
                               'hammer': True,
                               'score': ['0',
                                '2',
                                '0',
                                '0',
                                '0',
                                '0',
                                '1',
                                '1',
                                '1',
                                '0'],
                               'finalscore': '5'}),
                  'Matthew Hall': defaultdict(list,
                              {'href': 'event.php?view=Team&eventid=6400&teamid=144347&profileid=12435#1',
                               'hammer': False,
                               'score': ['0',
                                '0',
                                '4',
                                '0',
                                '0',
                                '1',
                                '0',
                                '0',
                                '0',
                                '2'],
                               'finalscore': '7'})}),
     defaultdict(list,
                 {'Dayna Deruelle': defaultdict(list,
                              {'href': 'event.php?view=Team&eventid=6400&teamid=144347&profileid=12435&eventid=6400&teamid=144346&profileid=26636#1',
                               'hammer': False,
                               'score': ['0',
                                '0',
                                '1',
                                '0',
                                '0',
                                '0',
                                '0',
                                'X',
                                '',
                                ''],
                               'finalscore': '1'}),
                  'Tyler Stewart': defaultdict(list,
                              {'href': 'event.php?view=Team&eventid=6400&teamid=144347&profileid=12435&eventid=6400&teamid=144352&profileid=12477#1',
                               'hammer': True,
                               'score': ['0',
                                '2',
                                '0',
                                '2',
                                '1',
                                '1',
                                '4',
                                'X',
                                '',
                                ''],
                               'finalscore': '10'})}),
     defaultdict(list,
                 {'Mark Kean': defaultdict(list,
                              {'href': 'event.php?view=Team&eventid=6400&teamid=144352&profileid=12477&eventid=6400&teamid=144348&profileid=25961#1',
                               'hammer': True,
                               'score': ['2',
                                '0',
                                '1',
                                '0',
                                '0',
                                '0',
                                '1',
                                '3',
                                'X',
                                ''],
                               'finalscore': '7'}),
                  'Jason March': defaultdict(list,
                              {'href': 'event.php?view=Team&eventid=6400&teamid=144352&profileid=12477&eventid=6400&teamid=144350#1',
                               'hammer': False,
                               'score': ['0',
                                '0',
                                '0',
                                '0',
                                '2',
                                '1',
                                '0',
                                '0',
                                'X',
                                ''],
                               'finalscore': '3'})}),
     defaultdict(list,
                 {'Richard Krell': defaultdict(list,
                              {'href': 'event.php?view=Team&eventid=6400&teamid=144350&profileid=0&eventid=6400&teamid=144349&profileid=25962#1',
                               'hammer': True,
                               'score': ['2',
                                '0',
                                '1',
                                '0',
                                '2',
                                '1',
                                '1',
                                'X',
                                '',
                                ''],
                               'finalscore': '7'}),
                  'Rob Ainsley': defaultdict(list,
                              {'href': 'event.php?view=Team&eventid=6400&teamid=144350&profileid=0&eventid=6400&teamid=144345&profileid=15779#1',
                               'hammer': False,
                               'score': ['0',
                                '0',
                                '0',
                                '1',
                                '0',
                                '0',
                                '0',
                                'X',
                                '',
                                ''],
                               'finalscore': '1'})})]



A boxscore is returned as a dictionary of team names, game information dictionary key, value pairs.

Each game information dictionary contains:

* 'href' key with a corresponding string value of CurlingZone IDs identifying the team.
* 'hammer' key with corresponding boolean value of whether or not that team started the game with hammer.
* 'score' key with corresponding list of string value of end-by-end results for that team.
* 'finalscore' key with corresponding final score for the team.

Individual boxscores can be accessed through the `get_boxscore_from` method.

```python
boxscore = linescore_page.get_boxscore_from(cz_game_id = 1)
boxscore
```




    defaultdict(list,
                {'Wayne Tuck Jr.': defaultdict(list,
                             {'href': 'event.php?view=Team&eventid=6400&teamid=144353&profileid=12486#1',
                              'hammer': True,
                              'score': ['0',
                               '2',
                               '0',
                               '0',
                               '0',
                               '0',
                               '1',
                               '1',
                               '1',
                               '0'],
                              'finalscore': '5'}),
                 'Matthew Hall': defaultdict(list,
                             {'href': 'event.php?view=Team&eventid=6400&teamid=144347&profileid=12435#1',
                              'hammer': False,
                              'score': ['0',
                               '0',
                               '4',
                               '0',
                               '0',
                               '1',
                               '0',
                               '0',
                               '0',
                               '2'],
                              'finalscore': '7'})})



`cz_game_id` argument corresponds to the number the boxscore appears in on the linescore page.

The LinescorePage object contains these properties which details information on the boxscores:

* event_name
* event_date
* draw

```python
print(linescore_page.event_name,',',linescore_page.event_date,',' ,linescore_page.draw)
```

    Ontario Tankard - Open Qualifier , Jan 17 - 19, 2020 , Draw: 2
    

For convenience, upon instantiation of a `LinescorePage` object, a `NormalizedBoxscore` instance for each boxscore is created. A `NormalizedBoxscore` holds the same information as a boxscore dictionary with two new pieces of information added: 
1. The hammer progression for both teams throughout the game, i.e. who had hammer in what end.
2. Each team's relative score, i.e. who was up/down X after end Y.

```python
normalized_boxscore = linescore_page.get_normalized_boxscore_from(cz_game_id = 1)
normalized_boxscore
```




    NormalizedBoxscore(boxscore=defaultdict(<class 'list'>, {'Wayne Tuck Jr.': defaultdict(<class 'list'>, {'href': 'event.php?view=Team&eventid=6400&teamid=144353&profileid=12486#1', 'hammer': True, 'score': ['0', '2', '0', '0', '0', '0', '1', '1', '1', '0'], 'finalscore': '5'}), 'Matthew Hall': defaultdict(<class 'list'>, {'href': 'event.php?view=Team&eventid=6400&teamid=144347&profileid=12435#1', 'hammer': False, 'score': ['0', '0', '4', '0', '0', '1', '0', '0', '0', '2'], 'finalscore': '7'})}))



A `NormalizedBoxscore` object holds two `NormalizedHalfBoxscore` instances. 

```python
normalized_boxscore.normalized_half_boxscore_pair[0]
```




    NormalizedHalfBoxscore(team_name='Wayne Tuck Jr.', href='event.php?view=Team&eventid=6400&teamid=144353&profileid=12486#1', hammer=True, score=['0', '2', '0', '0', '0', '0', '1', '1', '1', '0'], finalscore='5', hammer_progression=[True, False, True, True, True, True, False, False, False, True], normalized_score=[0, 2, -2, -2, -2, -3, -2, -1, 0, -2])



For Wayne Tuck Jr. the `hammer_progression` attribute can be interpreted as follows: 

* After end 1: Wayne had hammer
* After end 2: Wayne didn't have hammer
* After end 3: Wayne had hammer
* And so on and so forth..

```python
normalized_boxscore.normalized_half_boxscore_pair[-1]
```




    NormalizedHalfBoxscore(team_name='Matthew Hall', href='event.php?view=Team&eventid=6400&teamid=144347&profileid=12435#1', hammer=False, score=['0', '0', '4', '0', '0', '1', '0', '0', '0', '2'], finalscore='7', hammer_progression=[False, True, False, False, False, False, True, True, True, False], normalized_score=[0, -2, 2, 2, 2, 3, 2, 1, 0, 2])



For Matthew Hall, the `normalized_score` attribute can be interpreted as follows:

* After end 1: Matthew was tied.
* After end 2: Matthew was down 2.
* After end 3: Matthew was up 2.
* And so on and so forth..

You'll also notice the `NormalizedBoxscore` object has a guid property which identifies that two `NormalizedHalfBoxscore` belong to the same game.

```python
normalized_boxscore.guid
```




    147003164415014657208020002953825569462



czapi's `get_flat_boxscores_from` function takes a `LinescorePage` as an argument and returns a (flat) nested list object of all the boxscore information on the linescore page. This nested list object can be ingested into a pandas DataFrame or pushed to a SQL database.

```python
api.get_flat_boxscores_from(linescore_page = linescore_page)
```




    [['Wayne Tuck Jr.',
      'event.php?view=Team&eventid=6400&teamid=144353&profileid=12486#1',
      True,
      ['0', '2', '0', '0', '0', '0', '1', '1', '1', '0'],
      '5',
      [True, False, True, True, True, True, False, False, False, True],
      [0, 2, -2, -2, -2, -3, -2, -1, 0, -2],
      147003164415014657208020002953825569462],
     ['Matthew Hall',
      'event.php?view=Team&eventid=6400&teamid=144347&profileid=12435#1',
      False,
      ['0', '0', '4', '0', '0', '1', '0', '0', '0', '2'],
      '7',
      [False, True, False, False, False, False, True, True, True, False],
      [0, -2, 2, 2, 2, 3, 2, 1, 0, 2],
      147003164415014657208020002953825569462],
     ['Dayna Deruelle',
      'event.php?view=Team&eventid=6400&teamid=144347&profileid=12435&eventid=6400&teamid=144346&profileid=26636#1',
      False,
      ['0', '0', '1', '0', '0', '0', '0', 'X', '', ''],
      '1',
      [False, True, False, True, True, True, True],
      [0, -2, -1, -3, -4, -5, -9],
      36967671048107339783546455733355689426],
     ['Tyler Stewart',
      'event.php?view=Team&eventid=6400&teamid=144347&profileid=12435&eventid=6400&teamid=144352&profileid=12477#1',
      True,
      ['0', '2', '0', '2', '1', '1', '4', 'X', '', ''],
      '10',
      [True, False, True, False, False, False, False],
      [0, 2, 1, 3, 4, 5, 9],
      36967671048107339783546455733355689426],
     ['Mark Kean',
      'event.php?view=Team&eventid=6400&teamid=144352&profileid=12477&eventid=6400&teamid=144348&profileid=25961#1',
      True,
      ['2', '0', '1', '0', '0', '0', '1', '3', 'X', ''],
      '7',
      [True, True, False, False, True, True, False, False],
      [2, 2, 3, 3, 1, 0, 1, 4],
      255290136142512439531859386627462583284],
     ['Jason March',
      'event.php?view=Team&eventid=6400&teamid=144352&profileid=12477&eventid=6400&teamid=144350#1',
      False,
      ['0', '0', '0', '0', '2', '1', '0', '0', 'X', ''],
      '3',
      [False, False, True, True, False, False, True, True],
      [-2, -2, -3, -3, -1, 0, -1, -4],
      255290136142512439531859386627462583284],
     ['Richard Krell',
      'event.php?view=Team&eventid=6400&teamid=144350&profileid=0&eventid=6400&teamid=144349&profileid=25962#1',
      True,
      ['2', '0', '1', '0', '2', '1', '1', 'X', '', ''],
      '7',
      [True, True, False, True, False, False, False],
      [2, 2, 3, 2, 4, 5, 6],
      163493561909482716838197553130549415110],
     ['Rob Ainsley',
      'event.php?view=Team&eventid=6400&teamid=144350&profileid=0&eventid=6400&teamid=144345&profileid=15779#1',
      False,
      ['0', '0', '0', '1', '0', '0', '0', 'X', '', ''],
      '1',
      [False, False, True, False, True, True, True],
      [-2, -2, -3, -2, -4, -5, -6],
      163493561909482716838197553130549415110]]



## About czapi
czapi is a Python library for scraping curling linescores.
