import random

def Mode_Check(mode:str):
    if mode.isdigit() and 2 < int(mode) < 7:
        return True
    return False

def Input_Check(play_detail:dict):
    if play_detail['user_input'].isdigit() and len(set(int(s) for s in play_detail['user_input']))  == play_detail['game_mode']:
            return True
    return False

def Answer_Make(mode:int):
    answer = random.sample(range(0, 10), mode)
    return answer

def Answer_Check(play_detail:dict):
    play_detail['play_times'] = play_detail.get('play_times',0) + 1
    a = b = 0
    game_end = False
    for n,i in enumerate(play_detail['user_input']):
        if int(i) == play_detail['game_answer'][n]:
            a += 1
        elif int(i) in play_detail['game_answer']:
            b += 1                    
    if a == play_detail['game_mode']:
        play_detail['game_message'] = f'第 {play_detail["play_times"]} 回合 : {play_detail["user_input"]} 恭喜答對!!'
        game_end = True
    else:
        play_detail['game_message'] = f'第 {play_detail["play_times"]} 回合 : {play_detail["user_input"]} 為 {a} A {b} B'
    return play_detail,game_end
