# ⏱️ ⏰ 🕰️ Fastimer

[![PyPi](https://img.shields.io/pypi/v/fastimer)](https://pypi.org/project/fastimer/) [![mypy](https://github.com/vkostyanetsky/Fastimer/actions/workflows/mypy.yml/badge.svg)](https://github.com/vkostyanetsky/Fastimer/actions/workflows/mypy.yml) [![pylint](https://github.com/vkostyanetsky/Fastimer/actions/workflows/pylint.yml/badge.svg)](https://github.com/vkostyanetsky/Fastimer/actions/workflows/pylint.yml) [![black](https://github.com/vkostyanetsky/Fastimer/actions/workflows/black.yml/badge.svg)](https://github.com/vkostyanetsky/Fastimer/actions/workflows/black.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

It is a little CLI timer to track fasts, designed specifically to help you monitor your fasting intervals.  

## 😮 What's this for?

Yeah, there are plenty of apps like this one, you are right.

To come clear, I wrote this one simply out of annoyance when [Zero](https://www.zerolongevity.com/) app for Android once again refused to show me statistics for a date. I was tapping on calendar inside the application, but it was doing nothing ¯\\\_(ツ)\_/¯

Have no idea what was wrong with it. Anyway, the problem is not that hard, so I just wrote my own timer.

## 🙃 How to install it?

I have nothing to surprise you here:

```commandline
pip install fastimer
```

## 🙂 How to use it?

Run the app in the directory where you want to store your data:

```commandline
fastimer
```

The script shows you a menu with three commands available: 

1. Start New Fast
2. Fasts Browser
3. Statistics  

### Start New Fast

Something is obvious: the first command starts a new fast. It asks you for a number of hours you will be hungry and turns the timer on.

You can control the active fast directly from the main menu. Have a look:

```
  ┌───────────────────────────────────────────────────────────────────────────┐
  │  FASTING TIMER                                                            │
  ├───────────────────────────────────────────────────────────────────────────┤
  │                                                                           │
  │    ACTIVE FAST                                                            │
  │                                                                           │
  │    From: Wed, 19:33                                                       │
  │    Goal: Thu, 09:33 (14 hours)                                            │
  │                                                                           │
  │    #######--------------------------------- 19.2%                         │
  │                                                                           │
  │    Elapsed time:   02h 41m                                                │
  │    Remaining:      11h 19m                                                │
  │                                                                           │
  ├───────────────────────────────────────────────────────────────────────────┤
  │                                                                           │
  │    1 - Stop Active Fast                                                   │
  │    2 - Fasts Browser                                                      │
  │    3 - Statistics                                                         │
  │    4 - Exit                                                               │
  │                                                                           │
  └───────────────────────────────────────────────────────────────────────────┘
```

So, you can when you started, when you are going to finish, elapsed time, remaining time and something that looks like a progress bar to visualize your spilled blood, sweat, and tears :-)

## Stop Active Fast

When the fast is active, the command `Stop Active Fast` appears and allows you to stop your fast when you decided to do so.

It asks you whether you want to finish your fast or cancel it. Finishing means you wish to store the fast in the app history; cancelling means you wish to delete the information about this fast by a reason. 

### Fasts Browser

The `Fasts Browser` command of the main menu allows you to browse through your fasts.

By default, it shows you the very last one, but you switch fasts by using `Left` and `Right` buttons on your keyboard. 

```
COMPLETED FAST

From: Mon, 19:27
Goal: Tue, 09:27 (14 hours)

Fasting zones:

- Anabolic:     from Mon, 19:27
- Catabolic:    from Mon, 23:27 <-- you were here
- Fat burning:  from Tue, 11:27
- Ketosis:      from Tue, 19:27
- Anabolic:     from Thu, 19:27

######################################## 101.3%

Elapsed time:   14h 11m
Extra time:     00h 11m

Press [Left] and [Right] to switch fasts.
Press [Esc] to return to the main menu.
```

### Statistics

The `Statistics` command shows you statistical data and earned [achievements](Achievements.md).

For instance:

```
FASTING STATISTICS

Completed Fasts:         33 out of 34
Total Fasting Time:      437h 26m
Average Fast Length:     13h 15m
Longest Fast Length:     18h 12m
Longest Fasting Streak:  20 days
Current Fasting Streak:  3 days

Achievements:
- COPPER WALKER (level 2 badge out of 9). Twenty five fasts completed!
- COPPER MAN OF HABIT (level 2 badge out of 9). Ten completed fasts in a row!
```

## 😌 Questions 

### Where can I see or edit my fasts?

The script stores all the fasts in `fasts.yaml` file in the working directory (where you run the timer). The file is quite human-readable, so you can just open it in your lovely text editor.

For instance, the completed fast in the journal looks like this:

```yaml
- length: 16
  started: 2022-07-20 19:59:14
  stopped: 2022-07-21 12:00:33
```

The first parameter is the length of the fast, the second is the start date of this, and the third is the completion date.

For an active fast, the `stopped` parameter is omitted.
