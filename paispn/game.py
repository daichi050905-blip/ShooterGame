import pyxel

Width = 160
High = 120
Enemy_count = 60
Attack_count = 10
START_SCENE = "start"
PLAY_SCENE = "play"

#敵のクラス
class Enemy:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def update(self):
    #上下移動
    if pyxel.frame_count % Attack_count == 0:
      if 1 <= self.y <= 103:
        self.y += pyxel.rndi(-10, 10)
      elif self.y <= 0:
        self.y += 10
      elif self.y >= 104:
        self.y -= 10

  def draw(self):
    pyxel.blt(130, self.y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)

#攻撃のクラス
class Attack:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def update(self):
    if self.x <= 147:
      self.x += 1

  def draw(self):
    pyxel.blt(self.x + 5, self.y, 0, 8, 0, 8, 5, pyxel.COLOR_BLACK)

#敵攻撃のクラス
class Enemy_attack:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def update(self):
    if self.x >= 6:
      self.x -= 1

  def draw(self):
    pyxel.blt(self.x, self.y, 0, 8, 5, 8, 3, pyxel.COLOR_BLACK)

class App:
  def __init__(self):
    pyxel.init(Width, High, title = "シューティングゲーム")
    pyxel.mouse(True)
    self.current_scene = START_SCENE
    pyxel.load("my_resource.pyxres")
    self.enemys = []
    self.attacks = []
    self.enemy_attacks = []
    self.takasa = 60
    self.score = 0
    self.mine_high = 52
    self.is_collision = False
    pyxel.run(self.update, self.draw)

  def reset_play_scene(self):
    self.enemys = []
    self.attacks = []
    self.enemy_attacks = []
    self.takasa = 60
    self.score = 0
    self.mine_high = 52
    self.is_collision = False

  def update_start_scene(self):
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
      self.current_scene = PLAY_SCENE

  def update_play_scene(self):
    #敵の出現
    if pyxel.frame_count % Enemy_count == 0:
      self.enemys.append(Enemy(130, pyxel.rndi(0, High - 16)))

    if pyxel.btn(pyxel.KEY_UP) and 1 <= self.takasa <= 112:
      self.takasa -= 1
      self.mine_high -= 1
    elif pyxel.btn(pyxel.KEY_DOWN) and 0 <= self.takasa <= 111:
      self.takasa += 1
      self.mine_high += 1

    #攻撃の出現
    if pyxel.frame_count % Attack_count == 0:
      self.attacks.append(Attack(10, self.takasa))

    #攻撃の上下移動
    for attack in self.attacks.copy():
      attack.update()
       
      if attack.x >= 147:
        self.attacks.remove(attack)

    #敵の上下移動
    for enemy in self.enemys.copy():
      enemy.update()

      #敵の攻撃出現
      if pyxel.frame_count % Attack_count == 0:
        self.enemy_attacks.append(Enemy_attack(128 , enemy.y))

      #味方攻撃の当たり判定
      for i in range(len(self.attacks) - 1):
        if enemy.x - 5 <= self.attacks[i].x <= enemy.x + 11 and enemy.y <= self.attacks[i].y <= enemy.y + 16 and enemy in self.enemys:
          self.enemys.remove(enemy)

          self.score += 1
    
    #敵攻撃の上下移動
    for enemy_attack in self.enemy_attacks.copy():
      enemy_attack.update()

      #敵攻撃の消滅
      if enemy_attack.x == 5:
        self.enemy_attacks.remove(enemy_attack)

      #ゲームオーバー判定
      if 4 <= enemy_attack.x <= 8 and self.mine_high <= enemy_attack.y <= self.mine_high + 16:
        self.is_collision = True

    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.is_collision:
      self.reset_play_scene()
      self.is_collision = False
      self.current_scene = START_SCENE

  def update(self):
    #ゲームをやめる
    if pyxel.btnp(pyxel.KEY_ESCAPE):
      pyxel.quit()

    if self.current_scene == START_SCENE:
      self.update_start_scene()
    elif self.current_scene == PLAY_SCENE:
      self.update_play_scene()

  def draw_start_scene(self):
    pyxel.cls(pyxel.COLOR_BLACK)
    pyxel.text(50, 60, "Click To Start!!", pyxel.COLOR_PINK)

  def draw_play_scene(self):
    pyxel.cls(pyxel.COLOR_GRAY)
    for enemy in self.enemys:
      enemy.draw()
    for attack in self.attacks:
      attack.draw()
    for enemy_attack in self.enemy_attacks:
      enemy_attack.draw()
    pyxel.text(150, 0, str(self.score), pyxel.COLOR_GREEN)
    pyxel.blt(8, self.mine_high , 0, 32, 0, 16, 16, pyxel.COLOR_BLACK)

  def draw_gameover_scene(self):
    pyxel.cls(pyxel.COLOR_RED)
    pyxel.text(60, 60, "gameover", pyxel.COLOR_BROWN)
    
  def draw(self):
    if self.current_scene == START_SCENE and self.is_collision == False:
      self.draw_start_scene()
    elif self.current_scene == PLAY_SCENE and self.is_collision == False:
      self.draw_play_scene()
    elif self.is_collision:
      self.draw_gameover_scene()
   


App()