init python:
    import sys
    import os
    import json
    from chatgpt import *
    from chatgpt.utils import *
    from chatgpt.affection_system import *

    def read_file(file_path):
        with renpy.file(file_path) as f:
            return f.read().decode('utf-8')
        
    def reset_affection():
        persistent.love = [0]

    def get_ai_response(user_input):
        messages.append({"role": "user", "content": user_input})
        updated_messages = completion(messages, api_key)
        ai_response = updated_messages[-1]["content"]
        
        # 호감도 처리 및 응답 정제
        clean_response, affection_change = process_ai_response(ai_response, persistent.love)
        
        return clean_response, affection_change


    try:
        with open(config.gamedir + "/config.json", "r") as f:
            config_data = json.load(f)
            api_key = config_data.get("OPENAI_API_KEY")
    except:
        api_key = None

    if not api_key:
        api_key = os.environ.get('OPENAI_API_KEY')

init:
    screen stat_overlay:
        frame:
            padding (15, 15)
            background "#4f5a6680"
            align (1.0, 0.0)
            xmaximum 250
            ymaximum 200 
            vbox:
                text "{color=#FA5858}Jacks{/color}{space=15}[persistent.love[0] if persistent.love else 0]" size 16
                bar:
                    value persistent.love[0]
                    range 100
                    style "fixed_bar"
                text " " size 3

init -5 python:
    style.fixed_bar = Style(style.default)
    style.fixed_bar.xmaximum = 200
    style.fixed_bar.ymaximum = 15
    style.fixed_bar.left_gutter = 0
    style.fixed_bar.right_gutter = 0
    style.fixed_bar.left_bar = Frame("images/bar_full.png", 0, 0)
    style.fixed_bar.right_bar = Frame("images/bar_empty.png", 0, 0)

# 호감도 수치 초기화
default persistent.love = [0]

# 게임에서 사용할 캐릭터를 정의합니다.
define J = Character("Jacks", color="#FA5858")
define narrator = Character(None, kind=nvl)
define player = Character("[player_name]")

image bg1 = "backgrounds/church.png"
image bg2 = "backgrounds/room.png"
image bg3 = "backgrounds/room2.png"

image bad1 = "backgrounds/bad1.png"
image bad2 = "backgrounds/bad2.png"
image bad3 = "backgrounds/bad3.png"

image Jacks_top = "images/Jacks/Jacks_top.png"
image Jacks_full = "images/Jacks/Jacks_full.png"
image Jacks_full2 = im.FactorScale("images/Jacks/Jacks_full.png", 1.7)
image Jacks_closeup = im.Crop(im.FactorScale("images/Jacks/Jacks_full.png", 2.0), (0, 0, 800, 600))


screen show_date(day):
    zorder 100
    frame:
        xfill True
        yfill True
        background "#000000"
        vbox:
            xalign 0.5
            yalign 0.5
            text day:
                size 100
                color "#FFFFFF"
                text_align 0.5
                xalign 0.5


screen game_over_screen():
    modal True
    
    # 전체 화면을 덮는 검은색 배경
    add "black" # 또는 Solid("#000000")
    
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30

        text "GAME OVER" size 100 xalign 0.5 color "#FFFFFF"
        textbutton "Return to Main Menu" text_color "#FFFFFF" xalign 0.5 action Return()


# 여기에서 부터 게임이 시작됩니다.
label start:
    # 호감도 창 표시
    $ reset_affection()
    $ persistent.love = [0] if not persistent.love else persistent.love
    show screen stat_overlay
    
    "Game start"
    "Game name is: 'Once Upon a Broken Heart'"
    
    $ messages = [{"role": "system", "content": "You are a helpful assistant."}]

    # 게임 시작 시 모든 엔딩을 읽어옵니다
    $ all_bad_endings = read_and_format_endings("docs/1~3 bad ending.txt")
    $ background = read_file("docs/Background.txt")
    python:
        for line in background.splitlines():
            renpy.say(narrator, line)
    nvl clear

    $ player_name = renpy.input("Enter your name:")
    $ player_name = player_name.strip()

    # 여기서 scene 전환
    call day1
    $ result = check_affection(1, persistent.love[0])
    if result:
        jump expression result
    
    call day2
    $ result = check_affection(2, persistent.love[0])
    if result:
        jump expression result

    call day3
    $ result = check_affection(3, persistent.love[0])
    if result:
        jump expression result


    # 게임 플레이 감사 멘트
    $ credit = read_file("docs/Thank you for play demo.txt")
    python:
        for line in credit.splitlines():
            renpy.say(narrator, line)
    
    return


label change_day(new_day):
    # 화면을 어둡게 만듭니다
    scene black with fade
    
    # 새로운 날짜를 표시합니다
    show screen show_date(new_day)
    with dissolve
    
    # 3초 동안 날짜를 보여줍니다
    $ renpy.pause(2.5, hard=True)
    
    # 날짜 화면을 서서히 사라지게 합니다
    hide screen show_date
    with dissolve
    
    # 게임 화면으로 돌아갑니다
    scene
    with fade
    return

label chat_loop(times):
    $ chat_count = 0
    while chat_count < times:
        $ user_input = renpy.input("What do you want to say? (Type 'end' to end the conversation)")
        $ user_input = user_input.strip()

        if user_input.lower() == 'end':
            J "The conversation has passed."
            return
        
        $ ai_response, affection_change = get_ai_response(user_input)
        J "[ai_response]"

        $ chat_count += 1

    narrator "The conversation has ended."
    nvl clear
    return

label day1:
    call change_day("Day 1")
    scene bg1

    $ narrator_lines = [
        "You approach a cathedral in the abandoned Temple District of Valenda.", 
        "People used to come to worship at the Fated churches, but all you can see now are buildings and streets long forgotten.", 
        "As you step into the The Prince of Hearts' church, you are reminded of the warning your mother always told you: Never make a bargain with a Fate.", 
        "As you approach the altar to pray, you notice a young man in the corner.", 
        "Everything from his clothes to his hair is disheveled. You begin to whisper your prayers, but you can feel the man watching you." 
    ]
    python:
        for line in narrator_lines:
            narrator(line)
    nvl clear
    show Jacks_full at center with dissolve
    menu:
        "Don't you know it is rude to stare?":
            $ persistent.love[0] += 5
            $ response, _ = get_ai_response("Don't you know it is rude to stare?")
            player "Don't you know it is rude to stare?"
            J "[response]"

            menu:
                "We're in the Prince of Hearts' church. You should be more respectful.":
                    $ persistent.love[0] += 1
                    $ response, _ = get_ai_response("We're in the Prince of Hearts' church. You should be more respectful.")
                    player "We're in the Prince of Hearts' church. You should be more respectful."
                    J "[response]"

                "I've come to get help from The Prince of Hearts-Not to be flirted with.":
                    $ persistent.love[0] += 3
                    $ response, _ = get_ai_response("I've come to get help from The Prince of Hearts. Not to be flirted with.")
                    player "I've come to get help from The Prince of Hearts. Not to be flirted with."
                    J "[response]"
                        
                    menu:
                        "You're the Prince of Hearts?":
                            $ response, _ = get_ai_response("You're the Prince of Hearts?")
                            player "You're the Prince of Hearts?"
                            J "[response]"

        "Are you here to seek the Prince of Hearts' help too?":
            $ persistent.love[0] += 1
            $ response, _ = get_ai_response("Are you here to seek the Prince of Hearts' help too?")
            player "Are you here to seek the Prince of Hearts' help too?"
            J "[response]"

            menu:
                "Are you really the Prince of Hearts?":
                    $ response, _ = get_ai_response("Are you really the Prince of Hearts?")
                    player "Are you really the Prince of Hearts?"
                    J "[response]"

    $narrator_lines = [
        "The Prince of Hearts approaches you nonchalantly.", 
        "While he still looks disheveled there is something hauntingly beautiful about him.", 
        "Could he truly be as cruel and wicked as the legends say? There's only one way to find out."
    ]
    python:
        for line in narrator_lines:
            narrator(line)
    nvl clear
    hide Jacks_full with dissolve
    show Jacks_top at right with dissolve

    menu:
        "I need your help.":
            $ response, _ = get_ai_response("I need your help.")
            player "I need your help."
            J "[response]"

    narrator "You can question him few times when chance comes."
    nvl clear
    call chat_loop(1)  # 1회 대화

    narrator "Make him an offer."
    nvl clear

    call chat_loop(2)  # 2회 대화

    $ narrator_lines = [
        "Three broken-heart shaped scars appear on your wrists sealing the deal you've made with the Fate.", 
        "You find yourself standing alone in the cathedral and you get the eerie feeling that you bargained away something you can't get back.",
        "Day 1 ends."
    ]
    python:
        for line in narrator_lines:
            narrator(line)
    nvl clear
    return

label day2:
    call change_day("Day 2")
    scene bg2

    $ narrator_lines = [
        "A week has passed since you saw Jacks.", 
        "As you sit on your bed, you stroke the tiny scars on your wrists pondering when the Fate will return to collect your debt.", 
        "Ice cold fingers grab the back of your neck, snapping you out of your trance."
    ]
    python:
        for line in narrator_lines:
            narrator(line)
    nvl clear

    show Jacks_full at left with dissolve


    # 여기서 가까워 지는 효과 이미지 추가 (필요)

    menu:
        "Where have you been? It's been a week.":
            $ response, _ = get_ai_response("Where have you been? It's been a week.")
            player "Where have you been? It's been a week."
            J "[response]"
        "It's about time you showed up. I've been waiting.":
            $ response, _ = get_ai_response("It's about time you showed up. I've been waiting.")
            player "It's about time you showed up. I've been waiting."
            J "[response]"

    menu:
        "Can I ask you a question?":
            $ response, _ = get_ai_response("Can I ask you a question?")
            player "Can I ask you a question?"
            J "[response]"

        "I need answers now.":
            $ response, _ = get_ai_response("I need answers now.")
            player "I need answers now."
            J "[response]"

    $ narrator_lines = [
        "This is your chance.", 
        "You can ask him about these scars or what he really wants from you.", 
        "Or should you use this as a chance to get to know him better?"
    ]
    python:
        for line in narrator_lines:
            narrator(line)
    nvl clear

    hide Jacks_full
    show Jacks_top at right with dissolve

    call chat_loop(6)  # 6회 대화

    $ narrator_lines = [
        "Somewhat satisfied with his answers and noticing that he seems eager to leave, you change the topic.", 
        "Though you're not sure what topics of conversation are popular among the Fates.", 
        "You spot your favorite book on the nightstand. Perhaps The Prince of Hearts enjoys fairy tales."
    ]
    python:
        for line in narrator_lines:
            narrator(line)
    nvl clear
    
    menu:
        "Are you familiar with “The Ballad of the Archer and the Fox”?":
            $ response, _ = get_ai_response("Are you familiar with “The Ballad of the Archer and the Fox”?")
            player "Are you familiar with “The Ballad of the Archer and the Fox”?"
            J "[response]"

        "Do you believe in fairy tales?":
            $ response, _ = get_ai_response("Do you believe in fairy tales?")
            player "Do you believe in fairy tales?"
            J "[response]" 

    $ narrator_lines = [
        "As quick as he appeared, Jacks is gone again.", 
        "Next time you see him, you have feeling it won't be for polite conversation.",
        "Day 2 ends."
    ]
    python:
        for line in narrator_lines:
            narrator(line)
    nvl clear
    return  

label day3:
    call change_day("Day 3")
    scene bg3

    $ narrator_lines = [
        "You awaken in the middle of the night in an unfamiliar room.", 
        "You notice a trail of apple cores leading towards the fire place.", 
        "Jacks stands there, face aglow from the fire burning the hearth."
    ]
    python:
        for line in narrator_lines:
            narrator(line)
    nvl clear

    show Jacks_full at center with dissolve

    menu:
        "Why have you brought me here?":
            $ response, _ = get_ai_response("Why have you brought me here?")
            player "Why have you brought me here?"
            J "[response]"

        "Why are there so many apples on the floors?":
            $ response, _ = get_ai_response("Why are there so many apples on the floors?")
            player "Why are there so many apples on the floors?"
            J "[response]"

    hide Jacks_full
    show Jacks_top at right with dissolve

    call chat_loop(10)  # 10회 대화
    
    $ narrator_lines = [
        "You feel a cold breeze on your shoulders and suddenly you are back in your own room.", 
        "You look around for Jacks, but he is nowhere to be found.", 
        "As you make your way to your bed, you spot an apple on your pillow.", 
        "Upon further inspection, you find a note.", 
        "“Are you prepared for what lies ahead, Little Fox? For the next time we meet, our true adventure will begins.”",
        "Day 3 ends."
    ]
    python:
        for line in narrator_lines:
            narrator(line)
    nvl clear
    return



label random_bad_ending:
    $ bad_ending = renpy.random.choice(["bad_ending_1", "bad_ending_2", "bad_ending_3"])
    call expression bad_ending
    return

label bad_ending_1:
    scene bad1
    $ number, title, sentences = all_bad_endings[0]
    "[number] [title]"
    python:
        for sentence in sentences:
            renpy.say(narrator, sentence)
    nvl clear
    $ reset_affection()
    jump game_over

label bad_ending_2:
    scene bad2
    $ number, title, sentences = all_bad_endings[1]
    "[number] [title]"
    python:
        for sentence in sentences:
            renpy.say(narrator, sentence)
    nvl clear
    $ reset_affection()
    jump game_over

label bad_ending_3:
    scene bad3
    $ number, title, sentences = all_bad_endings[2]
    "[number] [title]"
    python:
        for sentence in sentences:
            renpy.say(narrator, sentence)
    nvl clear
    $ reset_affection()
    jump game_over

label game_over:
    call screen game_over_screen
    return