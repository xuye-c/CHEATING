import pygame
import os
import random
import math
import time
#倒计时
clock = pygame.time.Clock()
COUNTDOWN_TIME = 214 #3.5min
end_time = time.time()+ COUNTDOWN_TIME
#读入题库
data = []
with open("qa.txt") as file:
    for line in file.readlines():
        line = line.strip("\n")
        data.append(line)
#分类，题库和答案库一一对应
qa_index = 0
q_library=[]
a_library=[]
while(qa_index < len(data)):
    q_library.append(data[qa_index])
    a_library.append(data[qa_index+1])
    qa_index = qa_index + 2
library_size = len(q_library)               #题库大小

#gaming start
pygame.init()
#窗口设置
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CHEATING")
#图片导入
script_dir = os.path.dirname(os.path.abspath(__file__))
zl1 = pygame.image.load(os.path.join(script_dir, "img/zl/zl1.png"))
zl2 = pygame.image.load(os.path.join(script_dir, "img/zl/zl2.png"))
lj1 = pygame.image.load(os.path.join(script_dir, "img/professor/lj1.png"))
lj2 = pygame.image.load(os.path.join(script_dir, "img/professor/lj2.png"))
lj3 = pygame.image.load(os.path.join(script_dir, "img/professor/lj3.png"))
SIT = pygame.image.load(os.path.join(script_dir, "img/sit.png"))
DESK = pygame.image.load(os.path.join(script_dir, "img/desk.png"))
PAPERTOSS = pygame.image.load(os.path.join(script_dir, "img/papertoss.png"))
TXTBOX = pygame.image.load(os.path.join(script_dir, "img/text.png"))
win = pygame.image.load(os.path.join(script_dir, "img/win.png"))
#调整图片大小
Z1 = pygame.transform.scale(zl1, (SCREEN_WIDTH/10, SCREEN_HEIGHT/10))
Z2 = pygame.transform.scale(zl2, (SCREEN_WIDTH/10, SCREEN_HEIGHT/10))
l1 = pygame.transform.scale(lj1, (1.5*SCREEN_WIDTH/10, 1.5*SCREEN_HEIGHT/10))
l2 = pygame.transform.scale(lj2, (1.5*SCREEN_WIDTH/10, 1.5*SCREEN_HEIGHT/10))
l3 = pygame.transform.scale(lj3, (1.5*SCREEN_WIDTH/10, 1.5*SCREEN_HEIGHT/10))
sit = pygame.transform.scale(SIT, (1.125*SCREEN_WIDTH/10, 1.35*SCREEN_HEIGHT/10))
desk = pygame.transform.scale(DESK, (1.125*SCREEN_WIDTH/10, 1.35*SCREEN_HEIGHT/10))
pt = pygame.transform.scale(PAPERTOSS, (SCREEN_WIDTH/30, SCREEN_HEIGHT/30))
WIN = pygame.transform.scale(win, (SCREEN_HEIGHT, SCREEN_WIDTH))
#图片分组
ZL = [Z1, Z2, sit]
LJ = [l1,l2, l3]
BG = pygame.image.load(os.path.join(script_dir, "img/bg/bg.png"))
# 背景大小适配窗口
BG1 = pygame.transform.scale(BG, (SCREEN_HEIGHT, SCREEN_WIDTH))

#音频导入
pygame.mixer.init()
spy = pygame.mixer.Sound(os.path.join(script_dir, "sounds/spy.wav"))
spy1 = pygame.mixer.Sound(os.path.join(script_dir, "sounds/spy1.wav"))
spy2 = pygame.mixer.Sound(os.path.join(script_dir, "sounds/spy2.wav"))
yaho = pygame.mixer.Sound(os.path.join(script_dir, "sounds/yaho.wav"))
fail = pygame.mixer.Sound(os.path.join(script_dir, "sounds/fail.wav"))
win = pygame.mixer.Sound(os.path.join(script_dir, "sounds/win.wav"))
bgclock = pygame.mixer.Sound(os.path.join(script_dir, "sounds/clockt.wav"))

class zhongli:
    origin_x = SCREEN_WIDTH*0.6
    origin_y = SCREEN_HEIGHT*0.6
    def __init__(self):
        self.image = ZL[0]
        self.h = self.image.get_height()
        self.w = self.image.get_width()
        self.zl_rect = self.image.get_rect()
        self.zl_rect.x = self.origin_x
        self.zl_rect.y = self.origin_y
        self.stepindex = 8
        self.upperb = self.zl_rect.y>SCREEN_HEIGHT*0.4-0.5*self.h
        self.lowerb = self.zl_rect.y<SCREEN_HEIGHT-self.h
        self.rightb = self.zl_rect.x>0 and self.zl_rect.x>(-self.zl_rect.y+0.8*SCREEN_HEIGHT)/math.sqrt(5)
        self.leftb = self.zl_rect.x<SCREEN_WIDTH-self.w and self.zl_rect.x<SCREEN_WIDTH-(0.8*SCREEN_HEIGHT-self.zl_rect.y)/math.sqrt(5)-self.w
    
    def update(self, userInput, SCREEN):
        global sitting, ANSWER_SURFACE
        self.upperb = self.zl_rect.y>SCREEN_HEIGHT*0.5-0.5*self.h
        self.lowerb = self.zl_rect.y<SCREEN_HEIGHT-self.h
        self.leftb = self.zl_rect.x>0 and self.zl_rect.x>(-self.zl_rect.y+0.8*SCREEN_HEIGHT)/math.sqrt(5)
        self.rightb = self.zl_rect.x<SCREEN_WIDTH-self.w and self.zl_rect.x<SCREEN_WIDTH-(0.8*SCREEN_HEIGHT-self.zl_rect.y)/math.sqrt(5)-self.w

        if userInput[pygame.K_SPACE] and sitting and not ANSWER_SURFACE:
                sitting = False
                self.image = ZL[0]
        if sitting == False:
            if userInput[pygame.K_UP] and self.upperb and self.leftb and self.rightb:
                self.zl_rect.y = self.zl_rect.y - self.stepindex
            elif userInput[pygame.K_DOWN] and self.lowerb:
                self.zl_rect.y = self.zl_rect.y + self.stepindex
            elif userInput[pygame.K_LEFT] and self.leftb:
                self.zl_rect.x = self.zl_rect.x - self.stepindex
            elif userInput[pygame.K_RIGHT] and self.rightb:
                self.zl_rect.x = self.zl_rect.x + self.stepindex
            self.draw(SCREEN)
        elif sitting == True:
            self.image = ZL[2]
            self.zl_rect.x = 0.5*SCREEN_WIDTH-self.image.get_width()*0.5
            self.zl_rect.y = 0.6*SCREEN_HEIGHT
            self.draw(SCREEN)
        #if self.zl_rect.colliderect(professor.rect) : print("#detected")
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.zl_rect.x, self.zl_rect.y))
    
class professor:
    def __init__(self):
        #self.spy = False
        self.image = LJ[0]
        self.w = self.image.get_width()
        self.rect = self.image.get_rect()
    def update(self, SPYING):
        self.image = LJ[SPYING]
        self.draw(SCREEN)
    def draw(self, SCREEN):
        self.rect.topleft = (0.5 * SCREEN_WIDTH - 0.5 * self.w, 0.3 * SCREEN_HEIGHT)
        SCREEN.blit(self.image, self.rect.topleft)

class Desk:
    def __init__(self):
        self.image = desk
        self.rect = self.image.get_rect()
    def update(self, zl, SCREEN):
        global sitting
        if self.rect.colliderect(zl.zl_rect): 
            sitting = True
            zl.update(userInput, SCREEN)
    def draw(self, SCREEN):
        self.rect.topleft = (0.5*SCREEN_WIDTH-self.image.get_width()*0.5, 0.6*SCREEN_HEIGHT)
        SCREEN.blit(self.image, self.rect.topleft)

class cheatsheet:
    def __init__(self):
        self.image = pt
        self.rect = self.image.get_rect()
        self.h = self.image.get_height()
        self.w = self.image.get_width()
        self.rect.x = SCREEN_WIDTH*0.4
        self.rect.y = SCREEN_HEIGHT*0.6
    #def update(self):
        self.upperb = SCREEN_HEIGHT*0.5-0.5*self.h
        self.lowerb = SCREEN_HEIGHT-self.h
        self.rect.y = random.uniform(self.lowerb, self.upperb)

        self.leftb = max(0, (-self.rect.y+0.8*SCREEN_HEIGHT)/math.sqrt(5))
        self.rightb = min(SCREEN_WIDTH-(0.8*SCREEN_HEIGHT-self.rect.y)/math.sqrt(5)-self.w, SCREEN_WIDTH-self.w)
        self.rect.x = random.uniform(self.leftb, self.rightb)
    def draw(self, SCREEN):
        self.rect.topleft = (self.rect.x, self.rect.y)
        SCREEN.blit(self.image, self.rect.topleft)

class q_paper:
    def __init__(self):
        #global answer_sheet
        self.questions = q_library                      #问题池
        self.answers = a_library                        #答案池
        self.size = len(self.questions)                 #池子大小
        self.a_sheet = answer_sheet.copy()              #可选答案
        self.hints = answer_sheet.copy()                #小抄池
        #self.count = 0                                  #回答次数
        #self.a_sheet = ["a", "b", "c", "d"]
        #self.hints = ["a", "b", "c", "d"]
    def newquestion(self):
        #global answer_sheet
        self.key = random.randint(0, self.size-1)         #抽取问题
        #self.a_sheet = ["a", "b", "c", "d"]              #重置答案池
        self.a = self.answers[self.key]                 #获取问题答案
        self.q = self.questions[self.key]               #获取问题题面
        self.a_sheet = answer_sheet.copy()
        self.hints = answer_sheet.copy()

        #self.hints = ["a", "b", "c", "d"]
        #print(self.q, "#",self.a, "#", self.hints)
        self.hints.remove(self.a)                        #小抄池子里的排除选项不能有正确答案
        self.questions.pop(self.key)                    #避免抽出重复的问题
        self.answers.pop(self.key)                      #已经出过的问题对应的答案也删掉
        #self.count = 0                                  #重置已经回答的次数
        self.size = len(self.questions)                                 
    def get_hints(self):                                #在获得新问题之后，获取本卷小抄池
        return self.hints
    def get_keys(self):                                 #返回题号
        return self.key
    def get_answersheet(self):
        return self.a_sheet 
    def update_hints(self):
        if(len(self.hints)>=1):
            #获取本次小抄的排除项
            h_index = random.randint(0,len(self.hints)-1)
            self.h = self.hints[h_index]
            self.hints.remove(self.h)
            self.a_sheet.remove(self.h)
        else:
            self.h = " "
    def display_hint(self):
        #显示小抄
        f_h = pygame.font.Font('freesansbold.ttf', 25)
        if self.h == " ": h_txt = f_h.render("You've got all hints for this question", True, (0,0,0))
        else: h_txt = f_h.render("Hint: "+str(self.h)+" is incorrect.", True, (0,0,0))
        htxt_rect = h_txt.get_rect()
        htxt_rect.center = (0.5*SCREEN_WIDTH, 0.9*SCREEN_HEIGHT)
        SCREEN.blit(h_txt, htxt_rect)

        
    def draw(self, SCREEN):
        global my_answer, ideas
        font = pygame.font.Font('freesansbold.ttf', 23)
        rec_font = pygame.font.Font('freesansbold.ttf', 19)
        font1 = pygame.font.Font('freesansbold.ttf', 30)
        f_instr = pygame.font.Font('freesansbold.ttf', 15)

        question = self.q.split("#", 1)
        the_q0 = font.render(str(question[0]), True, (0, 0, 0)) #题面
        the_q1 = rec_font.render(str(question[1]), True, (0, 0, 0)) #选项
        Title = font1.render("Q:", True, (0, 0, 0))
        if ideas:
            record = rec_font.render("your answer: "+ str(my_answer) +"   ; idea left: 1", True, (0,0,0))
        else:
            record = rec_font.render("your answer: "+ str(my_answer) +"   ; idea left: 0", True, (0,0,0))
        instr1 = f_instr.render("press space key to roll your rubber dice", True, (100, 100, 100))
        instr2 = f_instr.render("press Y to confirm your answer, or you can pick up some hints to get ideas", True, (100, 100, 100))

        qRect0 = the_q0.get_rect()
        qRect1 = the_q1.get_rect()
        QRect = Title.get_rect()
        rec_rect = record.get_rect()
        instr1_rect = instr1.get_rect()
        instr2_rect = instr2.get_rect()

        width = max(qRect0.width, qRect1.width, QRect.width, instr1_rect.width, instr2_rect.width, rec_rect.width)
        height = QRect.height+ qRect0.height+ qRect1.height+instr1_rect.height+ instr2_rect.height+rec_rect.height
        txtbox = pygame.transform.scale(TXTBOX, (width+200, height+80))#根据题面尺寸调整背景
        bg_rect = txtbox.get_rect()

        bg_rect.center = ((SCREEN_WIDTH // 2)+1, SCREEN_HEIGHT // 4)
        QRect.center = ((SCREEN_WIDTH // 2)-bg_rect.width//2.5, (SCREEN_HEIGHT // 4)-40)
        qRect0.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 4)-15)
        qRect1.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 4)+15)
        rec_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 4)+50)
        instr1_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 4)+70)
        instr2_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 4)+85)

        SCREEN.blit(txtbox, bg_rect)
        SCREEN.blit(the_q0, qRect0)
        SCREEN.blit(the_q1, qRect1)
        SCREEN.blit(Title, QRect)
        SCREEN.blit(record, rec_rect)
        SCREEN.blit(instr1, instr1_rect)
        SCREEN.blit(instr2, instr2_rect)
def main():
    global sitting, userInput, counting, SPYING, answer_sheet, ANSWER_SURFACE, my_answer, ideas, score, q_number, pickup, hdisplay_count, q_amount
    answer_sheet = ["a", "b", "c", "d"]         #所有可能的答案
    ideas = True
    my_answer = ""
    ANSWER_SURFACE = False
    sitting = False
    run = True
    SPYING = 0
    score = 0
    q_number = 0
    pickup = 0
    q_amount = 10                                       #总题数
    hdisplay_count = 0

    font = pygame.font.Font('freesansbold.ttf', 20)
    Answered = True
    clock = pygame.time.Clock()
    player = zhongli()
    lj = professor()
    table = Desk()
    quiz = q_paper()
    Hints = []
    counting = 0
    spy_test = random.randint(150, 300)
    alarming_stop = spy_test +90
    stop_spy = spy_test +180
    hdisplay = False
    spy_learn = 0

    def roll_rubber_dice(quiz):
        global hdisplay_count
        hdisplay_count = 0
        ansh = quiz.a_sheet
        a = len(ansh)   
        if a == 1: return ansh[0]
        index = random.randint(0, a-1)
        return ansh[index]
    def notice():
        global score, ideas, q_number
        scoretxt = font.render("Score: " + str(score)+"/"+str(q_amount), True, (220, 0, 50))
        if ideas:
            ideastxt = font.render("Idea: 1 ", True, (220, 0, 50))
        else:
            ideastxt = font.render("Idea: 0 ", True, (220, 0, 50))
        qtxt = font.render("Question number: " + str(q_number)+"/"+str(q_amount), True, (220, 0, 50))
        s_rect = scoretxt.get_rect()
        i_rect = ideastxt.get_rect()
        q_rect = qtxt.get_rect()
        s_rect.topright = (750, 60+ q_rect.height+i_rect.height)
        i_rect.topright = (750, 50+q_rect.height)
        q_rect.topright = (750, 40)
        SCREEN.blit(scoretxt, s_rect)
        SCREEN.blit(ideastxt, i_rect)
        SCREEN.blit(qtxt, q_rect)
    while run:
        counting = counting + 1
        clock.tick(30)
        remaining_time = max(0, int(end_time - time.time())) #剩余时间计算
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #开始
        userInput = pygame.key.get_pressed() #获取输入
        if spy_learn==0:
            #新手教程阶段
            if counting == spy_test:            #进入alarming
                SPYING = 1
                lj.update(SPYING)
                fonttxt = pygame.font.Font('freesansbold.ttf', 35)
                if not sitting: 
                    txt1 = fonttxt.render("You‘e going to get caught!", True, (220,0,50))
                    txt2 = fonttxt.render("Hurry up! Go back to your seat!", True, (220,0,50))
                else:
                    txt1 = fonttxt.render("Professor's spying!", True, (220,0,50))
                    txt2 = fonttxt.render("Keep in your seat!", True, (220,0,50))
                tr1 = txt1.get_rect()
                tr2 = txt2.get_rect()
                tr1.center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-25)
                tr2.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2+25)
                SCREEN.blit(txt1, tr1)
                SCREEN.blit(txt2,tr2)
                spy.play()
                pygame.display.flip()  # 刷新屏幕
                pygame.time.wait(4000)
            elif counting == alarming_stop:     #进入猎杀时刻
                SPYING = 2
                spy2.play(-1)
            if counting == stop_spy:            #继续玩手机
                spy2.stop()
                spy_learn = 1
                SPYING = 0
                counting = 0
                spy_test = random.randint(150, 300)
                alarming_stop = spy_test +90
                stop_spy = spy_test +180
        elif spy_learn != 0 :
                if counting == spy_test:            #进入alarming
                    SPYING = 1
                    spy1.play()
                elif counting == alarming_stop:     #进入猎杀时刻
                    spy1.stop()
                    spy2.play(-1)
                    SPYING = 2
                if counting == stop_spy:            #继续玩手机
                    SPYING = 0
                    counting = 0
                    spy2.stop()
                    spy_test = random.randint(150, 300)
                    alarming_stop = spy_test +90
                    stop_spy = spy_test +180
                
        
        #教室背景
        bg_rect = BG1.get_rect()
        SCREEN.blit(BG1, bg_rect)
        #画桌子
        if sitting == False:
            table.draw(SCREEN)
        table.update(player, SCREEN)
        #画longlong
        lj.update(SPYING)                         #lj图层应该再zl下面
        #lj.draw(SCREEN)                 
        #画zhongli
        player.update(userInput, SCREEN)
        #画纸团
        if len(Hints)==0:
            Hints.append(cheatsheet())
        for papertoss in Hints:
            papertoss.draw(SCREEN)
            if player.zl_rect.colliderect(papertoss.rect):
                pickup += 1
                yaho.set_volume(0.5)
                yaho.play()
                Hints.remove(papertoss)
        if pickup >= 3 and not ideas:
            pickup = 0
            quiz.update_hints()             #更新小抄池
            hdisplay = True
            ideas = True
        #显示倒计时
        rt_txt = font.render(f"Timer: {remaining_time} s left", True, (220, 0, 50))
        SCREEN.blit(rt_txt, (50,40))
        #显示小抄
        if hdisplay and hdisplay_count<=90:
            quiz.display_hint()
            hdisplay_count +=1
        elif hdisplay:
            hdisplay = False
            hdisplay_count = 0
        #答题界面
        if sitting and userInput[pygame.K_a]:
            ANSWER_SURFACE = True
        if sitting and ANSWER_SURFACE and userInput[pygame.K_q]:
            ANSWER_SURFACE = False
        if ANSWER_SURFACE:
            if Answered:
                quiz.newquestion()
                q_number +=1
                Answered = False
                pickup = 0
            elif userInput[pygame.K_SPACE] and ideas:
                my_answer = roll_rubber_dice(quiz)
                ideas = False
                hdisplay_count = 0
            elif userInput[pygame.K_y] and my_answer != "":
                if my_answer == quiz.a: score +=1
                Answered = True
                my_answer = ""
                ideas = True

            quiz.draw(SCREEN)
        #debug
        #pygame.draw.rect(SCREEN, (255, 0, 0), player.zl_rect, 2)  # zhongli 的矩形
        #pygame.draw.rect(SCREEN, (0, 255, 0), lj.rect, 2)  # professor 的矩形
        #pygame.draw.rect(SCREEN, (0, 0, 255), table.rect, 2)  # professor 的矩形
        notice()
        pygame.display.update()
        #结束触发
        if SPYING == 2 and not sitting:
            die()
            run = False
        #结算触发
        if q_number-1==q_amount:
            over(False)
            run = False
        if remaining_time==0:
            over(True)
            run = False
        

#主游戏开始前画面
def start():
    run = True
    bgclock.play(-1)
    while run:
        SCREEN.fill((255, 255, 255))
        bg_rect = BG1.get_rect()
        SCREEN.blit(BG1, bg_rect)
        font = pygame.font.Font('freesansbold.ttf', 30)
        font1 = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("Press any Key to Start", True, (0, 0, 0))
        instr = font.render("Hint:", True, (0, 0, 0))
        instr1= font1.render("1. Control the character with arrow keys.", True, (0,0,0))
        instr2= font1.render("2. Press on space key and use arrow keys to leave the seat.", True, (0,0,0))
        instr3= font1.render("3. Press 'A' to answer questions when you are in seat.", True, (0,0,0))
        instr5= font1.render("5. Pick up paperball when you have no ideas.", True, (0,0,0))
        instr4= font1.render("4. You can get an answer only if you have ideas", True, (0,0,0))
        instr6= font1.render("6. Dont' be discovered!!!", True, (0,0,0))

        textRect = text.get_rect()
        iRect = instr.get_rect()
        i1Rect = instr1.get_rect()
        i2Rect = instr2.get_rect()
        i3Rect = instr3.get_rect()
        i4Rect = instr4.get_rect()
        i5Rect = instr5.get_rect()
        i6Rect = instr6.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2-40)
        iRect.topleft = (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2-5)
        i1Rect.topleft = (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2+35)
        i2Rect.topleft = (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2+60)
        i3Rect.topleft = (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2+85)
        i4Rect.topleft = (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2+110)
        i5Rect.topleft = (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2+135)
        i6Rect.topleft = (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2+160)
        SCREEN.blit(text, textRect)
        SCREEN.blit(instr, iRect)
        SCREEN.blit(instr1, i1Rect)
        SCREEN.blit(instr2, i2Rect)
        SCREEN.blit(instr3, i3Rect)
        SCREEN.blit(instr4, i4Rect)
        SCREEN.blit(instr5, i5Rect)
        SCREEN.blit(instr6, i6Rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()
def die():
    SCREEN.fill((0,0,0))
    bgclock.stop()
    font = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render("YOU ARE CHEATING!!!", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(text, textRect)
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.quit()
def over(time_up):
    global score, q_amount
    spy2.stop()
    bgclock.stop()
    final_score = score/q_amount
    font = pygame.font.Font('freesansbold.ttf', 50)
    message = ""
    color = ()
    if(final_score<0.6): 
        color = (255, 0, 0)
        message = "YOU FAILED!!!"
        SCREEN.fill((0,0,0)) 
        fail.play()  
    else:
        color = (0,0,0)
        message = "You've got "+str(int(final_score*100))+" points!"
        SCREEN.fill((255, 255, 255))
        win_rect = WIN.get_rect()
        SCREEN.blit(WIN, win_rect)
        win.play()
    if time_up: message = "Time's Up! "+message
    result = font.render(message, True, color)
    resultRect = result.get_rect()
    resultRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(result, resultRect)
    
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.quit()
start()