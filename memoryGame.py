# 메모리 게임

# 라이브러리
import pygame
from random import *

# 레벨에 맞게 설정
def setup(level):
    # 숫자를 보여줄 시간
    global display_time
    display_time = 5 - (level // 3)
    display_time = max(display_time, 1) # 최소 1초 까지 보여주는걸로 설정

    # 숫자를 몇개 보여줄지
    number_count = (level // 3) + 5
    number_count = min(number_count, 20) # 최대 20개 까지 보여주는걸로 설정

    # grid 형태로 숫자를 랜덤으로 배치
    shuffle_grid(number_count)

# 숫자 섞기
def shuffle_grid(number_count):
    rows = 6
    columns = 6

    cell_size = 130 # 각 Grid cell 별 가로, 세로 크기
    button_size = 110 # Grid cell 내에 실제로 그려질 버튼 크기
    # 화면 850 x 850로 맞추기 위해서
    screen_left_margin = 35 # 전체 스크린 왼쪽 여백 
    screen_top_margin = 35 # 전체 스크린 위쪽 여백

    grid = [[0 for col in range(columns)] for row in range(rows)] # 6 x 6

    number = 1
    while number <= number_count:
        row_idx = randrange(0, rows) # row중 랜덤 선택
        col_idx = randrange(0, columns) # column중 랜덤 선택

        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number # 숫자 지정
            number += 1

            # 현재 grid cell 위치 기준으로 x, y 위치를 구함
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)

            # 숫자 버튼 만들기
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)
    
    # 배치된 랜덤 숫자 확인
    print(grid)

# 시작 화면 보여주기
def display_start_screen():
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5) # 반지름 60, 선 두께 5

    msg = game_font.render(f"{curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=start_button.center)
    screen.blit(msg, msg_rect)

# pos 에 해당하는 버튼 확인
def check_buttons(pos):
    global start, start_ticks # 전역 변수를 선언함

    if start: # 게임이 시작했을때
        check_number_buttons(pos)
    elif start_button.collidepoint(pos):
        start = True
        start_ticks = pygame.time.get_ticks() # 타이머 시작 (현재 시간을 저장)

def check_number_buttons(pos):
    global start, hidden, curr_level

    for button in number_buttons:
        if button.collidepoint(pos):
            if button == number_buttons[0]: # 올바른 숫자 클릭
                print("Correct")
                del number_buttons[0]
                if not hidden:
                    hidden = True # 숫자 숨김 처리
            else: # 잘못된 숫자 클릭
                game_over()
            break

    # 모든 숫자를 선택했을때 레벨을 높여서 다시 시작 화면
    if len(number_buttons) == 0:
        start = False
        hidden = False
        curr_level += 1
        setup(curr_level)

# 게임 종료 처리
def game_over():
    global running
    running = False

    # 메세지
    msg = game_font.render(f"Your level is {curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=(screen_width/2, screen_height/2))
    
    screen.fill(BLACK)
    screen.blit(msg, msg_rect)
                
# 게임 화면 보여주기
def display_game_screen():
    global hidden

    if not hidden:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> sec
        if elapsed_time > display_time:
            hidden = True

    for idx, rect in enumerate(number_buttons, start=1):
        if hidden: # 숨김 처리
            # 버튼 사각형 그리기
            pygame.draw.rect(screen, WHITE, rect)
        else:
            # 실제 숫자 텍스트
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)

# 초기화
pygame.init()
screen_width = 850 # 가로 크기
screen_height = 850 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("메모리 게임") # 타이틀
game_font = pygame.font.Font(None, 120) # 폰트

# 시작 버튼
start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_height - 120)

# 색깔 (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

number_buttons = [] # 플레이어가 눌러야 하는 버튼들
curr_level = 1 # 현재 레벨
display_time = None # 숫자를 보여주는 시간
start_ticks = None # 시간 계산 (현재 시간 정보를 저장)

# 게임 시작 여부
start = False
# 숫자 숨김 여부 (사용자가 1을 클릭했거나, 보여주는 시간 초과했을 때)
hidden = False

# 게임 시작 전에 게임 설정 함수 수행
setup(curr_level)

# 게임 루프
running = True # 게임이 실행중
while running:
    click_pos = None

    # 이벤트 루프
    for event in pygame.event.get(): # 이벤트 체크
        if event.type == pygame.QUIT: # 창이 닫힘
            running = False # 게임 실행중이 아님
        elif event.type == pygame.MOUSEBUTTONUP: # 사용자가 마우스를 클릭했을때
            click_pos = pygame.mouse.get_pos()
            print(click_pos)

    # 전체 화면을 어둡게
    screen.fill(BLACK)

    if start:
        display_game_screen() # 게임 화면 표시
    else:
        display_start_screen() # 시작 화면 표시

    # 사용자가 클릭한 좌표값
    if click_pos:
        check_buttons(click_pos)

    # 화면 업데이트
    pygame.display.update()

# 3초 뒤 꺼질수 있게 설정
pygame.time.delay(3000)

# 게임 종료
pygame.quit()