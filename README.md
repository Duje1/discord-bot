# Token Testing Branch

This branch exists to allow contributors to setup their environments and test their discord bot tokens in a minimal-overhead setup.

If you already have your bot registered & have the token, feel free to skip ahead.


## Registering Your Bot

Head to the [discord developer portal](https://discord.com/developers/applications), and click "New Application" in the upper right, and give it a name.

On the next page, you'll see a sidebar with a "Bot" option. Click this, and then click on "Add Bot". Proceed. 

On the next page, uncheck the option for making this a public bot (it should be the first option). While you are on this page, click the "copy" button to copy your discord token. We'll use this later.

On the sidebar, click OAuth2-  this is how we'll invite our bot. In the "scopes" group of checkboxes, select "Bot". This will open another set of checkboxes "bot permissions". Check all that apply (permissions the bot may need to perform its actions). I usually will not check "Administrator" or "Manage Server" on actual bots, in the event of a rogue bot, you at least don't have to worry about it breaking absolutely everything.

Finally, click the the "copy" button next to the url link in the upper group box, and paste this into your browser. You'll need to select the server to invite it to, and you'll need admin priviledges on this server in order to invite. Go ahead and invite it to our testing server (if you haven't already joined [here's an invite](https://discord.gg/NhhXgtM)). Click authorize, and you should see the bot join.

## Running The Bot

If you haven't already (if you're viewing this online), clone this repo. Then, switch to this branch (`token_testing`)-  `git checkout token_testing`.  Once on this branch, you'll find the bot's source code in `/src/bot.py`.

Modify the source code in `bot.py` to change the USERNAME global variable to your name, so that the bot will ping you specifically in its startup message (demonstrating that you got your test instance working).

Lastly, set an environment variable, `TEST_BOT_TOKEN`, with the value of the token you copied earlier in the setup / registration. In Linux, you can set this value in your `~/.bashrc`.  In linux, you must `export` a variable to make it propogate to child processes, in windows `set` will only set the variable for the current process, and you will need to use `setx` similarly to `export` in Linux.

With your environment variable set, you're almost ready to run the bot. You'll need the discord.py package installed. You can use `pip install discord.py` to get the package, or if your system has python2 and python3, you may need to use `pip3` to install it for the python3 install. Its recommended that you use some sort of virtual environment for your python installs so they don't become bloated with one-off packages. I'm not going to cover that here- that's another topic altogther.

With discord.py installed, run the `bot.py` script with a python3 interpreter, and you should see your bot pop online in the server, and also send a message to the server (and to your terminal). If so, congrats-  you're ready to contribute.
