# Home library

This is soft for librarian.

This project uses [ZomboDB](https://github.com/zombodb/zombodb)
(auto sync Postgres:10 +Elastic)

You need to install [Docker](https://www.docker.com/) on your system

# How to install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with 
old Python 2 setup) to install dependencies:

```bash
$ pip install -r requirements.txt
```

If you use ```pipenv```:

```bash
$ pipenv --three sync
```

# Quick start

First, you have to run ```docker-compouse.yml``` with command:

```bash
$ cd <library_dir> && sudo docker-compose up -d
```


### Fill database

```bash
$ python3 digger.py [--update] <path_to_file_or_dir>
```
Path to file or directory with ```.fb2 .fb2.zip .fb2.gz``` books

```-u --update``` update existed books

### Search book

```bash
$ python3 seeker.py [OPTIONS]
```

```-a, --author <author_name>```
  
```-n, --name <book_title>```

```-y, --year <year>```

```-l, --limit <number_book_for_print>```

```-s, --simple``` Return only book ID

### Delete book

```bash
$ python3 wiper.py [--number <number>] [--all]
```

```-n --number <book_ID_for_deletion>```

```-a --all``` delete all books and authors

## Pipenv
If you use ```pipenv```:
```bash
$ pipenv run <one_of_the_commands_above>
```

Running on Windows is similar.

*(Possibly requires call of 'python' executive instead of just 'python3'.)*

# Examples

```bash
$ pipenv run python seeker.py --author андрей --year 2009
1. Title: Вся правда о Русских: два народа
   ID: 7
   Year: 2009
   Authors: Андрей Михайлович Буровский

2. Title: Как закалялась сталь 2 и 1/2
   ID: 477
   Year: 2009
   Authors: Андрей Кочергин
```
```bash
$ pipenv run python seeker.py --name война --limit 2 --simple
1. 512
2. 172
```
```bash
$ pipenv run python seeker.py -y 1998
1. Title: Собрание сочинений в 5-ти томах. Том 3. Князь Велизарий.
   ID: 199
   Year: 1998
   Authors: Роберт Грейвз

2. Title: Беспорядочные связи
   ID: 485
   Year: 1998
   Authors: Лора Брэдли

3. Title: Сталинизм и война
   ID: 512
   Year: 1998
   Authors: Андрей Николаевич Мерцалов, Л А Мерцалова

```