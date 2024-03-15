# TypeRacer-bot-PoC

TypeRacer Vulnerability Proof of Concept (PoC)

## DISCLAIMER

This repository contains a Proof of Concept (PoC) intended solely for educational, research, and ethical testing purposes. It is strictly prohibited to use this software for any unauthorized testing, cheating, or any form of misuse on TypeRacer or any other platform. The purpose of this PoC is to demonstrate potential vulnerabilities within TypeRacer’s current system and to encourage stronger security measures.

The creator of this PoC does not endorse, encourage, or facilitate the misuse of this information in any way. Misuse of this information can result in legal consequences. The creator assumes no liability for actions taken by others based on the information provided.

## Ethical Considerations

The intention behind releasing this PoC is to contribute to the cybersecurity community's understanding of potential vulnerabilities in web applications and to promote a dialogue between security researchers and the affected platforms. This PoC is meant to be a starting point for discussions on how TypeRacer and similar platforms can enhance their security against automated bots and other forms of cheating.
Usage Notice

This code is provided for educational and ethical testing purposes only. It is the responsibility of the user to comply with all applicable laws and regulations. Any use of this code against any website or online service without explicit permission is strictly prohibited.

## Responsible Disclosure

I plan to engage in a responsible disclosure process with TypeRacer, sharing my findings in a manner that allows them to address the demonstrated vulnerabilities without putting their users at risk. This process is guided by the principle of minimizing potential harm and contributing to the overall security of the internet.
Conclusion

This PoC highlights the importance of continuous security assessments and the need for implementing robust measures to detect and prevent automated attacks. By sharing these findings, I hope to encourage TypeRacer and similar platforms to strengthen their defenses, thereby creating a safer and more secure online environment for all users.


## Background and Usage

Type Racer is a website available here: https://play.typeracer.com/ where you can practice your typing speed online by racing against others. 

I had a theory that it would be possible to write an exploit utilizing python that would be able to type any given text as a bot, simulating the speed of a human. If the speed is over 20% of your average, you will then be prompted with a Captcha. I believed that I would be able to beat the captcha utilizing AI, OCR technologies, utilizing the same typing method. This proved true.

I experimented with AI to solve the captchas and various other OCR tech, and ended up utilizing a previously trained LLM that was designed to read captchas. I could have improved this further but it was becoming a time sink. 

The script also automatically adjusts the speed so that it only ever types 15% faster than your previous top speed to avoid detection. I plan to responsibly disclose this shortly, as there are ways to prevent this type of attack. 

Script works as follows:

Preequiste: Ensure you have the msedgedriver in the root folder. This ensures that edge can be opened as the bot, which will then interact with the browser.

1. Input a dummy username and password into the identifed spot in the script.
2. Manually adjust speed, or leave automatic.
3. When running on auto speed, it will detect the speed that is displayed as the accounts average when logging in, and then apply a 15% increase to avoid detection.
4. Keep running the script and the speed will slowly start to increase in small increments.

Finally, I  know that similar bots have been built before. This project was undertaken in an effort to show how AI can be used to bypass captcha.
