# RoboType for Sublime Text 3

Emulate a human typing the content on your cliboard.

<img src="http://i.imgur.com/K348BTb.gif" width="480" height="360">

## Why?!

If you make screencasts, you'll understand.

## Configuration
You can control the speed of the typing, the likelihood of typos, and the responsiveness of the typist to typos. Typing speed is variable, so it is controlled by low and high thresholds.

* `robotype_keystroke_interval_low`: The fastest possible keystroke, in milliseconds. (Default is 10)
* `robotype_keystroke_interval_high`: The slowest possible keystroke, in millisecoinds. (Default is 100)
* `robotype_keystroke_accuracy`: A higher value results in more accurate typing. Perfect typing is 1. (Default is 30)
* `robotype_typo_reaction`: The latency in response to a typo. The higher the number, the longer it will take for the typist to discover the typo. A value of 1 will result in immediate discovery (i.e. the subsequent keystroke)

