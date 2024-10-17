import pygame
import random
import math

pygame.init()
pygame.mixer.init()  # 사운드 시스템 초기화

# 배경음악 로드 및 재생
pygame.mixer.music.load("C:\\Users\\82104\\Desktop\\gamecomponents\\gamebgm.mp3")  # 배경음악 파일 경로
pygame.mixer.music.set_volume(0.6)  # 음악 볼륨 설정 (0.0 ~ 1.0)
pygame.mixer.music.play(-1)  # -1은 무한 반복 재생

# 총소리 파일 로드
pistol_sound = pygame.mixer.Sound("C:\\Users\\82104\\Desktop\\gamecomponents\\pistolsound.mp3")
pistol_sound.set_volume(0.3)  # 총소리 볼륨 조절 (0.0 ~ 1.0)

# 전체 맵 크기 설정
map_width = 3000
map_height = 2000

# 화면 크기 설정
screen_width = 1280
screen_height = 840
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption('폭염에서 살아남기!')

# 폰트 설정
font = pygame.font.Font(None, 36)

# fps 설정
clock = pygame.time.Clock()

# 배경 이미지 불러오기
background = pygame.image.load("C:\\Users\\82104\\Desktop\\gamecomponents\\gamemap.png")
background = pygame.transform.scale(background, (map_width, map_height))  # 배경을 맵 크기에 맞게 조정

# 캐릭터 이미지 불러오기
character = pygame.image.load("C:\\Users\\82104\\Desktop\\gamecomponents\\gamecharacter.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = map_width / 2 - character_width / 2  # 맵 중앙에 위치
character_y_pos = map_height / 2 - character_height / 2

# 적(enemy) 이미지 불러오기
enemy_image = pygame.image.load("C:\\Users\\82104\\Desktop\\gamecomponents\\enemy.png")
enemy_size = enemy_image.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0, map_width - enemy_width)  # 랜덤 위치
enemy_y_pos = random.randint(0, map_height - enemy_height)

# 캐릭터 이동 속도
character_speed = 0.2

# 적 이동 속도
enemy_speed = 0.05

to_x = 0
to_y = 0

# 캐릭터 방향 (마지막으로 이동한 방향을 저장)
direction_x = 0
direction_y = -1  # 초기 방향 위쪽

# 카메라 좌표 (화면이 이동할 좌표)
camera_x = 0
camera_y = 0

# House image 불러오기 (이미지로 집을 그리기)
house_image = pygame.image.load("C:\\Users\\82104\\Desktop\\gamecomponents\\house.png")
house_image = pygame.transform.scale(house_image, (400, 500))  # house 이미지를 Rect 크기에 맞게 조정

# House area definition (position and size)
house = pygame.Rect(300, 300, 400, 500)

# 아이템 상자 이미지 불러오기
item_box_img = pygame.image.load("C:\\Users\\82104\\Desktop\\gamecomponents\\itembox.png")
item_box_img = pygame.transform.scale(item_box_img, (50, 50))

# icecream과 hot tea 아이템 이미지 불러오기
icecream_img = pygame.image.load("C:\\Users\\82104\\Desktop\\gamecomponents\\icecream.png")
icecream_img = pygame.transform.scale(icecream_img, (40, 40))
hot_tea_img = pygame.image.load("C:\\Users\\82104\\Desktop\\gamecomponents\\hot tea.png")
hot_tea_img = pygame.transform.scale(hot_tea_img, (40, 40))

# 아이템 상자 5개를 랜덤한 위치에 스폰 (집과 다른 아이템 영역 제외)
item_boxes = []
for _ in range(5):
    while True:
        item_x = random.randint(0, map_width - 50)  # 아이템 상자의 X 좌표를 랜덤으로 설정
        item_y = random.randint(0, map_height - 50)  # 아이템 상자의 Y 좌표를 랜덤으로 설정
        new_item_box = pygame.Rect(item_x, item_y, 50, 50)  # 아이템 상자의 Rect 정보 생성

        # 집이나 다른 아이템 상자와 겹치지 않으면 위치 확정
        if not new_item_box.colliderect(house) and new_item_box.collidelist(item_boxes) == -1:
            item_boxes.append(new_item_box)
            break  # 반복 종료, 아이템 스폰 완료


# 무기 이미지 불러오기
pistol_img = pygame.image.load("C:\\Users\\82104\\Desktop\\gamecomponents\\pistol.png")
machinegun_img = pygame.image.load("C:\\Users\\82104\\Desktop\\gamecomponents\\machinegun.png")
shotgun_img = pygame.image.load("C:\\Users\\82104\\Desktop\\gamecomponents\\shotgun.png")

# 무기 관련 변수
weapons = [pistol_img, machinegun_img, shotgun_img]
weapon_names = ["Pistol", "Machinegun", "Shotgun"]
weapon_slots = [None, None, None]  # 무기 슬롯 (최대 3개)
selected_weapon = None  # 현재 선택된 무기
# 무기별 데미지 설정
pistol_damage = 10
machinegun_damage = 5
shotgun_damage = 15


# 무기 스폰 위치 설정 (겹치지 않도록)
weapon_boxes = []
for i in range(3):
    while True:
        box_x = random.randint(0, map_width - 50)
        box_y = random.randint(0, map_height - 50)
        new_box = pygame.Rect(box_x, box_y, 50, 50)
        
        # 겹치는 무기가 있는지 확인
        if not new_box.collidelist(weapon_boxes) == -1:
            continue  # 무기가 겹치면 다시 스폰 위치를 설정

        # 집과도 겹치지 않도록 설정
        if not new_box.colliderect(house):
            weapon_boxes.append(new_box)
            break



# 총알 관련 변수
bullets = []
bullet_speed = 1.5  # 총알 속도 증가
bullet_cooldown = 200  # 총알 발사 간격 (밀리초)
last_bullet_time = 0

# 기온 및 체온 관련 변수
current_temp = 56.7  # 현재 기온
body_temp = 36.5  # 시작 체온 (변경 가능한 체온)
base_temp = 36.5  # 체온 상승을 시작하는 기준 체온
current_base_temp = base_temp  # 집 밖으로 나왔을 때 다시 시작할 체온
play_time = 0  # 플레이 시간
start_ticks = pygame.time.get_ticks()  # 시작 시간 저장
in_house = False  # 집 안에 있는지 여부를 추적

# 플레이 시간 추적을 위한 변수
play_start_ticks = pygame.time.get_ticks()  # 플레이 타임 시작 시간 (초기화되지 않음)
start_ticks = pygame.time.get_ticks()  # 체온 상승을 위한 시작 시간 (집에서 나올 때 갱신)
in_house = False  # 집 안에 있는지 여부를 추적

# 체온 상승 및 상태 변화 조건
blur_active = False  # 흐림 효과 활성화 여부

# 아이템 획득 관련 변수
popup_start_time = 0
popup_duration = 2000  # 2초 동안 팝업 표시
show_popup = False
popup_item = None

#체온 업데이트 함수
def update_body_temp(character_rect, house):
    global body_temp, character_speed, blur_active, in_house, start_ticks, current_base_temp

    # 캐릭터와 집의 충돌 감지를 위한 Rect 객체
    character_rect = pygame.Rect(character_x_pos, character_y_pos, character_width, character_height)

    # 캐릭터가 집 안에 있을 때
    if character_rect.colliderect(house):
        if not in_house:  # 처음 집에 들어가는 경우
            in_house = True
            current_base_temp = body_temp  # 현재 체온을 저장 (집 안에서 체온 유지)
            print(f"Entered house. Body temp: {body_temp}")
    else:
        # 캐릭터가 집 밖으로 나가는 순간 처리
        if in_house:  # 처음 집 밖으로 나가는 경우
            in_house = False
            start_ticks = pygame.time.get_ticks()  # 나오는 순간 시간을 새로 기록
            current_base_temp = body_temp  # 집에서 나오는 순간의 체온을 기준으로 다시 상승
            print(f"Left house. Reset start_ticks and current_base_temp. Body temp: {body_temp}")
    
    # 집 밖에 있을 때만 체온이 상승하도록 설정
    if not in_house:
        # 체온 상승을 집 밖에서 나오는 순간부터 시작
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # 경과 시간(초 단위)
        body_temp = current_base_temp + (elapsed_time / 60)  # 60초에 1도씩 체온 상승

    # 체온에 따른 상태 변화
    if body_temp < 38.5:
        character_speed = 0.2  # 체온이 38.5℃ 미만이면 이동 속도 정상
        blur_active = False  # 흐림 효과 해제
    elif 38.5 <= body_temp < 40.5:
        character_speed = 0.1  # 체온이 38.5℃ 이상이면 이동 속도 감소
        blur_active = False  # 흐림 효과 없음
    elif 40.5 <= body_temp < 41.5:
        character_speed = 0.1  # 체온이 40.5℃ 이상이면 이동 속도 유지
        blur_active = True  # 흐림 효과 활성화
    elif body_temp >= 41.5:
        draw_end_popup(play_time)  # 체온이 41.5℃가 되면 게임 종료
        pygame.time.delay(5000)
        pygame.quit()

# 화면 흐림 효과 함수
def apply_blur():
    blur_surface = pygame.Surface((screen_width, screen_height))
    blur_surface.set_alpha(128)  # 반투명한 검정색 레이어로 화면을 덮음
    blur_surface.fill((0, 0, 0))
    screen.blit(blur_surface, (0, 0))

# 텍스트 그리기 함수
def draw_text(text, font, color, surface, x, y):
    lines = text.splitlines()  # 여러 줄 처리
    for i, line in enumerate(lines):
        text_obj = font.render(line, True, color)
        surface.blit(text_obj, (x, y + i * 30))  # 줄마다 y 좌표를 다르게 설정하여 줄바꿈 적용

# 상태 메시지 업데이트 함수
def get_status_message(body_temp):
    if body_temp < 38.5:
        return "This is normal body temperature."
    elif 38.5 <= body_temp < 40.5:
        return "Early heatstroke!\nMovement speed becomes slower"
    elif body_temp >= 40.5:
        return "End of heatstroke!\nGame screen is blurry"

# 아이템 획득 팝업 그리기
def draw_item_popup(item_image, item_name):
    popup_width, popup_height = 300, 150
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2

    # 팝업 배경 그리기
    pygame.draw.rect(screen, (0, 0, 0), (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(screen, (255, 255, 255), (popup_x, popup_y, popup_width, popup_height), 5)

    # 텍스트 그리기 (아이템 획득)
    text = font.render(f"{item_name} 획득!", True, (255, 255, 255))
    screen.blit(text, (popup_x + 80, popup_y + 20))

    # 아이템 이미지 그리기
    screen.blit(item_image, (popup_x + 130, popup_y + 60))

# 무기 창 그리기 함수
def draw_weapon_slots():
    slot_size = 60
    for i in range(3):
        slot_x = 10 + i * (slot_size + 10)
        slot_y = screen_height - slot_size - 70
        # 선택된 무기 강조: 선택된 슬롯에 따라 테두리 색상을 다르게 설정
        if selected_weapon == weapon_slots[i]:
            border_color = (0, 255, 0)  # 초록색 테두리로 강조
        else:              
            border_color = (255, 255, 255)  # 기본 하얀색 테두리
        pygame.draw.rect(screen, border_color, (slot_x, slot_y, slot_size, slot_size), 3)
        draw_text(f"{i + 1}", font, (255, 255, 255), screen, slot_x + 20, slot_y - 20)
        if weapon_slots[i]:
            screen.blit(weapon_slots[i], (slot_x + 5, slot_y + 5))

# House area definition (position and size)
#house = pygame.Rect(300, 300, 400, 500)

# 집의 투명도를 위한 변수 추가
house_opacity = 255  # 기본 불투명 상태

# 종료 팝업 그리기 함수
def draw_end_popup(play_time):
    popup_width, popup_height = 400, 200
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2

    # 팝업 배경 그리기
    pygame.draw.rect(screen, (0, 0, 0), (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(screen, (255, 255, 255), (popup_x, popup_y, popup_width, popup_height), 5)

    # 종료 메시지 그리기
    text = font.render(f"Congratulations!", True, (255, 255, 255))
    screen.blit(text, (popup_x + 80, popup_y + 40))

    # 플레이 타임을 점수로 표시
    score_text = font.render(f"Your score = {int(play_time)} seconds", True, (255, 255, 255))
    screen.blit(score_text, (popup_x + 40, popup_y + 100))

    pygame.display.update()


# 추가할 변수들
in_house_time = 0  # 캐릭터가 집 안에 있을 때 시간을 추적
total_in_house_time = 0  # 집 안에 있는 누적 시간
next_spawn_time = 10  # 적이 스폰될 다음 기준 시간 (10초마다 적 스폰)

def spawn_enemy_away_from_player(character_x, character_y, min_distance=1100):
    while True:
        # 적을 랜덤한 위치에 스폰 (집 밖이어야 하고, 캐릭터와 거리가 일정 이상이어야 함)
        enemy_x_pos = random.randint(0, map_width - enemy_width)
        enemy_y_pos = random.randint(0, map_height - enemy_height)
        new_enemy_rect = pygame.Rect(enemy_x_pos, enemy_y_pos, enemy_width, enemy_height)

        # 적이 집 안에 스폰되지 않도록 확인
        if new_enemy_rect.colliderect(house):
            continue  # 집과 겹치면 다시 위치 설정

        # 캐릭터와의 거리가 충분히 떨어져 있는지 확인
        distance_to_player = math.hypot(enemy_x_pos - character_x, enemy_y_pos - character_y)
        if distance_to_player < min_distance:
            continue  # 캐릭터와 너무 가까우면 다시 위치 설정

        # 다른 적들과 겹치지 않도록 확인
        collision = False
        for enemy in enemies:
            existing_enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
            if new_enemy_rect.colliderect(existing_enemy_rect):
                collision = True
                break  # 다른 적과 겹치면 위치 다시 설정

        if not collision:
            # 겹치지 않고 캐릭터와도 일정 거리 이상 떨어지면 적 추가
            new_enemy = {"x": enemy_x_pos, "y": enemy_y_pos, "health": 100, "dead_time": None}
            enemies.append(new_enemy)
            break  # 적 스폰 완료

# 적 5마리 생성 (캐릭터와 일정 거리 이상 유지하며 생성)
enemies = []
for _ in range(5):
    spawn_enemy_away_from_player(character_x_pos, character_y_pos)

# 적(enemy) 체력
enemy_health = 100  # 기본 체력
enemy_respawn_time = 3000  # 적이 죽은 후 3초 후에 재스폰
enemy_dead_time = None  # 적이 죽은 시간을 저장할 변수

# 적 체력바 그리기 함수
def draw_enemy_health_bar(screen, x, y, health, max_health):
    BAR_WIDTH = 50  # 체력바의 너비
    BAR_HEIGHT = 5  # 체력바의 높이
    health_ratio = health / max_health  # 체력 비율

    # 체력바 배경 (빨간색)
    pygame.draw.rect(screen, (255, 0, 0), (x, y - 10, BAR_WIDTH, BAR_HEIGHT))

    # 현재 체력 (녹색, 체력 비율에 맞춰 너비가 변함)
    pygame.draw.rect(screen, (0, 255, 0), (x, y - 10, BAR_WIDTH * health_ratio, BAR_HEIGHT))



# 적들끼리의 충돌 확인 및 처리 함수
def handle_enemy_collisions():
    for i, enemy in enumerate(enemies):
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)

        for j, other_enemy in enumerate(enemies):
            if i != j:  # 자기 자신과는 충돌을 처리하지 않음
                other_enemy_rect = pygame.Rect(other_enemy["x"], other_enemy["y"], enemy_width, enemy_height)

                if enemy_rect.colliderect(other_enemy_rect):
                    # 적들이 충돌한 경우, 서로 반대 방향으로 밀어내기
                    overlap_dx = enemy["x"] - other_enemy["x"]
                    overlap_dy = enemy["y"] - other_enemy["y"]
                    overlap_distance = math.hypot(overlap_dx, overlap_dy)
                    
                    if overlap_distance != 0:
                        overlap_dx /= overlap_distance
                        overlap_dy /= overlap_distance
                        
                        # 충돌한 적들을 서로 반대 방향으로 밀어냄
                        enemy["x"] += overlap_dx * 0.5
                        enemy["y"] += overlap_dy * 0.5
                        other_enemy["x"] -= overlap_dx * 0.5
                        other_enemy["y"] -= overlap_dy * 0.5


# 게임 루프
running = True
while running:
    dt = clock.tick(60)  # FPS 설정
    current_time = pygame.time.get_ticks() / 1000  # 현재 시간을 초 단위로 변환

    # 체온이 41.5도 이상이면 게임 종료
    if body_temp >= 41.5:
        draw_end_popup(play_time)
        pygame.time.delay(5000)
        
        running = False  # 게임 루프 종료를 위한 플래그 설정
        continue  # 즉시 루프를 빠져나감

    # 키보드 입력 상태 저장
    keys = pygame.key.get_pressed()

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x = -character_speed
                if keys[pygame.K_UP]:
                    to_y = -character_speed
                    direction_x, direction_y = -1, -1  # 좌상
                elif keys[pygame.K_DOWN]:
                    to_y = character_speed
                    direction_x, direction_y = -1, 1   # 좌하
                else:
                    direction_x, direction_y = -1, 0  # 좌
            elif event.key == pygame.K_RIGHT:
                to_x = character_speed
                if keys[pygame.K_UP]:
                    to_y = -character_speed
                    direction_x, direction_y = 1, -1  # 우상
                elif keys[pygame.K_DOWN]:
                    to_y = character_speed
                    direction_x, direction_y = 1, 1   # 우하
                else:
                    direction_x, direction_y = 1, 0   # 우
            elif event.key == pygame.K_UP:
                to_y = -character_speed
                if keys[pygame.K_LEFT]:
                    to_x = -character_speed
                    direction_x, direction_y = -1, -1  # 좌상
                elif keys[pygame.K_RIGHT]:
                    to_x = character_speed
                    direction_x, direction_y = 1, -1   # 우상
                else:
                    direction_x, direction_y = 0, -1  # 상
            elif event.key == pygame.K_DOWN:
                to_y = character_speed
                if keys[pygame.K_LEFT]:
                    to_x = -character_speed
                    direction_x, direction_y = -1, 1   # 좌하
                elif keys[pygame.K_RIGHT]:
                    to_x = character_speed
                    direction_x, direction_y = 1, 1    # 우하
                else:
                    direction_x, direction_y = 0, 1    # 하

            if event.key == pygame.K_s:  # 's' 키를 눌렀을 때 아이템 획득
                # 캐릭터의 현재 위치를 기준으로 Rect 객체 생성
                character_rect = pygame.Rect(character_x_pos, character_y_pos, character_width, character_height)

                # 아이템 획득 후 상태 업데이트
                if event.key == pygame.K_s:  # 's' 키를 눌렀을 때 아이템 획득
                    # 캐릭터의 현재 위치를 기준으로 Rect 객체 생성
                    character_rect = pygame.Rect(character_x_pos, character_y_pos, character_width, character_height)

                    # 아이템 상자 획득 처리
                    for box in item_boxes[:]:
                        if character_rect.colliderect(box):
                            item_boxes.remove(box)  # 아이템 상자 제거

                            # 아이템 획득 시 체온 변화를 수정 (정확하게 체온 변화 반영)
                            if random.choice([True, False]):  # icecream 또는 hot tea 랜덤 획득
                                popup_item = icecream_img
                                body_temp -= 1  # 체온 1도 낮춤
                                current_base_temp -= 1  # 현재 체온 기준도 함께 낮춤
                                item_name = "Icecream"
                            else:
                                popup_item = hot_tea_img
                                body_temp += 1  # 체온 1도 올림
                                current_base_temp += 1  # 현재 체온 기준도 함께 높임
                                item_name = "Hot Tea"


                            # 아이템을 먹은 후 체온에 따른 상태를 즉시 반영
                            update_body_temp(character_rect, house)  # 아이템 사용 후 즉시 체온 상태 업데이트

                            popup_start_time = pygame.time.get_ticks()  # 팝업 시작 시간
                            show_popup = True  # 팝업 표시 활성화
                        

                # 무기 획득 처리
                for i, box in enumerate(weapon_boxes[:]):
                    if character_rect.colliderect(box):
                        if None in weapon_slots:  # 빈 슬롯이 있을 때만 무기 획득
                            slot_index = weapon_slots.index(None)
                            weapon_slots[slot_index] = weapons[i]  # 무기 이미지를 슬롯에 추가
                            item_name = weapon_names[i]  # 무기 이름 설정
                            popup_item = weapons[i]  # 팝업에 표시할 무기 이미지 설정
                            popup_start_time = pygame.time.get_ticks()
                            show_popup = True

                            # 무기 상자와 관련된 리스트에서 해당 무기를 제거
                            weapon_boxes.pop(i)
                            weapons.pop(i)
                            weapon_names.pop(i)
                            break  # 한 번에 하나의 무기만 획득

            # 무기 선택 (숫자 1, 2, 3)
            if event.key == pygame.K_1:
                selected_weapon = weapon_slots[0]
            elif event.key == pygame.K_2:
                selected_weapon = weapon_slots[1]
            elif event.key == pygame.K_3:
                selected_weapon = weapon_slots[2]

    # 무기 발사 처리 (대각선 방향 포함)
    if keys[pygame.K_SPACE] and selected_weapon:
        current_time = pygame.time.get_ticks()
        if current_time - last_bullet_time > bullet_cooldown:
            norm = math.hypot(direction_x, direction_y)  # 대각선 처리 시 방향 벡터의 크기를 구함
            direction_x_norm = direction_x / norm if norm != 0 else 0
            direction_y_norm = direction_y / norm if norm != 0 else 0
            # 총소리 재생 (총을 발사할 때)
            pistol_sound.play()

            if selected_weapon == pistol_img:
                bullet_cooldown = 300
                bullet_rect = pygame.Rect(character_x_pos + character_width / 2, character_y_pos + character_height / 2, 10, 10)
                bullets.append((bullet_rect, (direction_x_norm, direction_y_norm)))
            elif selected_weapon == machinegun_img:
                bullet_cooldown = 200
                for _ in range(3):  # machinegun은 빠르게 여러 발 발사
                    bullet_rect = pygame.Rect(character_x_pos + character_width / 2, character_y_pos + character_height / 2, 10, 10)
                    bullets.append((bullet_rect, (direction_x_norm, direction_y_norm)))
            elif selected_weapon == shotgun_img:
                bullet_cooldown = 400
                for angle in [-0.2, 0, 0.2]:  # shotgun은 세 발로 나뉘어서 발사
                    bullet_rect = pygame.Rect(character_x_pos + character_width / 2, character_y_pos + character_height / 2, 10, 10)
                    bullets.append((bullet_rect, (direction_x_norm + angle, direction_y_norm + angle)))
            last_bullet_time = current_time

    # Collision detection for the player with the house
    character_rect = pygame.Rect(character_x_pos, character_y_pos, character_width, character_height)
    if character_rect.colliderect(house):
        # Allow the player to move freely inside the house
        pass            
            
    # 키보드 뗄 때 이동 중지
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            to_x = 0
        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            to_y = 0

    # 캐릭터 이동
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    # 캐릭터와 집의 충돌 감지
    character_rect = pygame.Rect(character_x_pos, character_y_pos, character_width, character_height)
    # **충돌 후 체온 상태 업데이트**
    update_body_temp(character_rect, house)
    if character_rect.colliderect(house):
    # 캐릭터가 집 내부에 있을 때 집 투명도 조정
        house_opacity = 100  # 집을 반투명하게
    else:
        # 캐릭터가 집 밖에 있을 때 집을 원래대로
        house_opacity = 255  # 집을 불투명하게

    # 캐릭터가 집 안에 있는지 확인하고 시간을 추적
    if character_rect.colliderect(house):
        if not in_house:
            in_house = True
            in_house_time = pygame.time.get_ticks()  # 집에 들어간 시간 기록
    else:
        if in_house:
            in_house = False
            # 집에서 나올 때 누적 시간 업데이트
            total_in_house_time += (pygame.time.get_ticks() - in_house_time) / 1000  # 밀리초에서 초로 변환

    # 캐릭터가 집 안에 있을 때는 시간을 계속 누적
    if in_house:
        total_in_house_time += (pygame.time.get_ticks() - in_house_time) / 1000  # 현재 시간을 계속 누적
        in_house_time = pygame.time.get_ticks()  # 현재 시간을 업데이트


    # 누적 시간이 next_spawn_time을 넘으면 적을 추가로 스폰
    if total_in_house_time >= next_spawn_time:
        spawn_enemy_away_from_player(character_x_pos, character_y_pos)  # 캐릭터와 일정 거리 두고 적 추가 스폰
        next_spawn_time += 10  # 10초마다 적이 한 마리씩 추가 스폰


    # 적들끼리의 충돌 처리
    handle_enemy_collisions()

  


    # 맵 경계 처리 (캐릭터가 맵 밖으로 나가지 않게)
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > map_width - character_width:
        character_x_pos = map_width - character_width

    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > map_height - character_height:
        character_y_pos = map_height - character_height

    # 적이 캐릭터를 향해 다가가는 로직
    dx = character_x_pos - enemy_x_pos
    dy = character_y_pos - enemy_y_pos
    distance = math.hypot(dx, dy)
    if distance != 0:
        dx /= distance
        dy /= distance

    # 적의 위치를 캐릭터 방향으로 업데이트
    enemy_x_pos += dx * enemy_speed * dt
    enemy_y_pos += dy * enemy_speed * dt

    # 카메라가 캐릭터를 따라다니도록 설정 (화면의 중앙에 캐릭터를 맞춤)
    camera_x = character_x_pos - screen_width / 2 + character_width / 2
    camera_y = character_y_pos - screen_height / 2 + character_height / 2

    # 카메라가 맵 경계를 넘어가지 않게 조정  
    if camera_x < 0:
        camera_x = 0
    elif camera_x > map_width - screen_width:
        camera_x = map_width - screen_width

    if camera_y < 0:
        camera_y = 0
    elif camera_y > map_height - screen_height:
        camera_y = map_height - screen_height

    # 화면 그리기
    screen.blit(background, (-camera_x, -camera_y))  # 카메라에 따라 배경 이동
    screen.blit(character, (character_x_pos - camera_x, character_y_pos - camera_y))  # 캐릭터 그리기
    #screen.blit(enemy, (enemy_x_pos - camera_x, enemy_y_pos - camera_y))  # 적 그리기
    # 적의 체력바 그리기 (적이 그려진 후에 체력바 그리기)
    #draw_enemy_health_bar(screen, enemy_x_pos - camera_x, enemy_y_pos - camera_y, enemy_health, 100)
    # 집 그리기 (투명도 조정 적용)
    house_image_with_alpha = house_image.copy()  # house_image의 복사본을 만듦
    house_image_with_alpha.set_alpha(house_opacity)  # 투명도 적용 (집의 내부에 있으면 house_opacity 값을 낮춤)
    screen.blit(house_image_with_alpha, (house.x - camera_x, house.y - camera_y))  # 화면에 집 그리기





    # 아이템 상자 그리기
    for box in item_boxes:
        screen.blit(item_box_img, (box.x - camera_x, box.y - camera_y))

    # 무기 상자 그리기
    for i, box in enumerate(weapon_boxes):
        screen.blit(weapons[i], (box.x - camera_x, box.y - camera_y))

    bullets_to_remove = []  # 충돌한 총알이나 화면 밖으로 나간 총알을 저장할 리스트

    # 총알 이동 및 그리기
    for bullet in bullets[:]:  # bullets[:]는 bullets 리스트의 복사본을 사용하여 루프를 돈다.
        bullet_rect, bullet_direction = bullet
        bullet_rect.x += bullet_direction[0] * bullet_speed * dt * 1.5
        bullet_rect.y += bullet_direction[1] * bullet_speed * dt * 1.5

        # 총알이 화면 밖으로 나가면 제거할 목록에 추가
        if bullet_rect.x < 0 or bullet_rect.x > map_width or bullet_rect.y < 0 or bullet_rect.y > map_height:
            bullets_to_remove.append(bullet)  # 제거할 총알을 목록에 추가
            continue

        # 적들과 충돌 확인
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
            if bullet_rect.colliderect(enemy_rect):
                if bullet not in bullets_to_remove:  # 총알이 이미 제거 목록에 없는 경우만 추가
                    bullets_to_remove.append(bullet)
                enemy["x"] += bullet_direction[0] * 40  # 충돌 시 적을 밀어내는 효과
                enemy["y"] += bullet_direction[1] * 40
                # 무기별로 적의 체력 감소
                if selected_weapon == pistol_img:
                    enemy["health"] -= pistol_damage
                elif selected_weapon == machinegun_img:
                    enemy["health"] -= machinegun_damage
                elif selected_weapon == shotgun_img:
                    enemy["health"] -= shotgun_damage

        # 총알 그리기
        screen.blit(pygame.Surface((10, 10)), (bullet_rect.x - camera_x, bullet_rect.y - camera_y))

    # 루프가 끝난 후에 제거할 총알을 실제로 제거
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)

    # 적의 이동과 충돌 , 체력바
    for i, enemy in enumerate(enemies):
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)

        if enemy["health"] > 0:
            # 적이 캐릭터를 향해 이동하는 로직
            dx = character_x_pos - enemy["x"]
            dy = character_y_pos - enemy["y"]
            distance = math.hypot(dx, dy)  # 캐릭터와 적 사이의 거리 계산

            if distance != 0:
                dx /= distance  # 이동 방향 계산 (x축)
                dy /= distance  # 이동 방향 계산 (y축)

            # 적이 이동하려는 새로운 위치 계산
            new_x = enemy["x"] + dx * enemy_speed * dt
            new_y = enemy["y"] + dy * enemy_speed * dt

            # 적이 집에 충돌하는지 확인
            if enemy_rect.colliderect(house):
                # X축 충돌 처리
                new_x = enemy["x"] + dx * enemy_speed * dt
                temp_rect_x = pygame.Rect(new_x, enemy["y"], enemy_width, enemy_height)
                
                if temp_rect_x.colliderect(house):
                    if dx > 0 and enemy_rect.right > house.left:
                        new_x = house.left - enemy_width
                    elif dx < 0 and enemy_rect.left < house.right:
                        new_x = house.right
                enemy["x"] = new_x

                # Y축 충돌 처리
                new_y = enemy["y"] + dy * enemy_speed * dt
                temp_rect_y = pygame.Rect(enemy["x"], new_y, enemy_width, enemy_height)
                
                if temp_rect_y.colliderect(house):
                    if dy > 0 and enemy_rect.bottom > house.top:
                        new_y = house.top - enemy_height
                    elif dy < 0 and enemy_rect.top < house.bottom:
                        new_y = house.bottom
                enemy["y"] = new_y


            # 적 좌표 업데이트
            enemy["x"] = new_x
            enemy["y"] = new_y

            # 적 그리기 및 체력바 표시
            screen.blit(enemy_image, (enemy["x"] - camera_x, enemy["y"] - camera_y))
            draw_enemy_health_bar(screen, (enemy["x"] - camera_x), (enemy["y"] - camera_y), enemy["health"], 100)





        else:
            # 적이 죽은 후 리스폰 처리 (모든 적에게 적용)
            if enemy["dead_time"] is None:
                enemy["dead_time"] = pygame.time.get_ticks()
                print("적이 사망했습니다!")

            # 리스폰 시간이 지나면 기존 적을 리셋
            if pygame.time.get_ticks() - enemy["dead_time"] > enemy_respawn_time:
                # 적을 다시 스폰 위치로 이동 (캐릭터와 거리를 유지)
                enemy_x_pos, enemy_y_pos = random.randint(0, map_width - enemy_width), random.randint(0, map_height - enemy_height)
                while math.hypot(character_x_pos - enemy_x_pos, character_y_pos - enemy_y_pos) < 300 or pygame.Rect(enemy_x_pos, enemy_y_pos, enemy_width, enemy_height).colliderect(house):
                    enemy_x_pos, enemy_y_pos = random.randint(0, map_width - enemy_width), random.randint(0, map_height - enemy_height)

                # 적의 위치와 체력을 리셋
                enemy["x"] = enemy_x_pos
                enemy["y"] = enemy_y_pos
                enemy["health"] = 100  # 체력 초기화
                enemy["dead_time"] = None  # 리셋 완료



    # 흐림 효과 적용
    if blur_active:
        apply_blur()  # 체온이 40.5℃ 이상일 때 흐림 효과 유지

    # 텍스트 크기를 24로 줄이기
    font = pygame.font.Font(None, 24)  # 24는 텍스트 크기

    # 캐릭터의 체온에 따른 상태 메시지 가져오기
    status_message = get_status_message(body_temp)  # 여기서 상태 메시지 정의

    # 텍스트 그리기 (좌상단: 기온, 좌하단: 체온, 우하단: 플레이 타임)
    play_time = (pygame.time.get_ticks() - play_start_ticks) / 1000  # 게임 시작 이후 경과한 시간
    draw_text(f'Current Temperature: {current_temp}', font, (255, 255, 255), screen, 10, 10)
    draw_text(f'Body Temperature: {body_temp:.1f}', font, (255, 255, 255), screen, 10, screen_height - 50)
    draw_text(f'Play Time: {int(play_time)}s', font, (255, 255, 255), screen, screen_width - 200, screen_height - 50)
    draw_text(status_message, font, (255, 255, 255), screen, screen_width - 350, 10)

    # 무기 창 그리기
    draw_weapon_slots()
    
    # Draw the house (you can replace this with an image if you have one)
    #pygame.draw.rect(screen, (139, 69, 19), (house.x - camera_x, house.y - camera_y, house.width, house.height))


    # 팝업 창 그리기
    if show_popup:
        draw_item_popup(popup_item, item_name)
        # 팝업 표시 시간 초과 시 팝업 비활성화
        if pygame.time.get_ticks() - popup_start_time > popup_duration:
            show_popup = False

    # 체온 업데이트
    update_body_temp(character_rect, house)

    # 캐릭터와 모든 적의 충돌 확인
    character_rect = pygame.Rect(character_x_pos, character_y_pos, character_width, character_height)

    # 적들 중 하나라도 충돌하면 게임 종료
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
        if character_rect.colliderect(enemy_rect):
            print("충돌했어요!")
            # 종료 팝업 표시
            draw_end_popup(play_time)

            # 5초간 대기
            pygame.time.delay(5000)


            running = False
            break  # 충돌 시 루프 중단, 게임 종료

    pygame.display.update()
pygame.mixer.music.stop()  # 게임이 끝날 때 음악을 중지
pygame.quit()