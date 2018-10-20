from twython import Twython
import SisteKurs
import OppdaterCCY

##       LOGGER INN TWITTER          ##

twitter = Twython('dk66yh6jXRItq8u89EBH8OtJd','0sD5B2cY6O3zCy5V2NawNzV17uMd9cGmnvXR6IaIJcJf7wmU47', '882667244249133056-sjyOJ37OOhIY9FLMYShiVBO7tAt9vwu', 'rFbvUZmpkzX2MUQ1nlbiPVehZKrmZFfzZCOJ1bI94rkm8')

##      LAGER TEKST OG VISER HVA SOM SENDES TIL TWITTER            ##
tweeten = SisteKurs.RippleLastTweet

##      SETTER I GANG ROBOTEN            ##

twitter.update_status(status=tweeten)
