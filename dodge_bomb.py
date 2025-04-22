import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),  
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんrectまたは爆弾rect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True  # 判定変数
    # 横方向
    if rct.left < 0 or WIDTH < rct.right:  # 画面内だったら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate  


def gameover(screen: pg.Surface) -> None:
    kk_cry_img = pg.image.load("fig/8.png")  #泣いてるこうかとん
    brack_img = pg.Surface((WIDTH, HEIGHT))
    brack_img.set_alpha(50)
    fonto = pg.font.Font(None, 80)  # 文字
    txt = fonto.render("Game Over",
                       True, (255, 255, 255))
    
    screen.blit(brack_img, [0,0])
    screen.blit(kk_cry_img, [750, 300])
    screen.blit(kk_cry_img, [350, 300])
    screen.blit(txt, [420, 300])
    pg.display.update()
    time.sleep(5)
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #　こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    tmr = 0
    # 爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    # bb_rct.centerx = random~
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5

    # ゲームオーバー画面初期化
    
    

    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            # print("Game Over")
            # こうかとんレクとと爆弾レクとが重なっていたら
            gameover(screen)
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key , mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 左右方向
                sum_mv[1] += mv[1]  # 上下方向
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)  # こうかとん移動
        if check_bound(kk_rct) != (True, True):  # 画面の外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 画面内に戻す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  #左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
