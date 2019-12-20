import pygame
from pygame import *
import random
def main():


	pygame.init()

	#Criando a tela do jogo com 400 x 600 pixels
	screen = pygame.display.set_mode((400,600))

	#Nomeando o jogo
	pygame.display.set_caption('Crashing Drone')
	icon = pygame.image.load('img/drone.png')
	pygame.display.set_icon(icon)

	"""
		Constantes
	"""
	SCREEN_WIDTH = 400
	SCREEN_HEIGHT = 600
	SPEED = 10
	GRAVITY = 1
	GAME_SPEED = 10
	GROUND_WIDTH = 2* SCREEN_WIDTH
	GROUND_HEIGHT = 100
	PIPE_WIDTH = 100
	PIPE_HEIGHT = 500

	"""

			Classes

	"""

	#Criando o personagem: classe e Sprite

	class Drone(pygame.sprite.Sprite):

		def __init__(self):
			pygame.sprite.Sprite.__init__(self)

			#Criando o movimento estático do personagem
			self.images = [pygame.image.load('img/drone.png').convert_alpha(),
							pygame.image.load('img/drone2.png').convert_alpha()]

			self.current_image = 0
														#O convert_alpha faz com que o pygame interprete corretamente as transparências da imagem.
			self.image = pygame.image.load('img/drone.png').convert_alpha()
			self.mask = pygame.mask.from_surface(self.image)
			#Rect carrega o atual posicionamento da figura e o seu tamanho. Importante para realizar updates na figura (Personagem).
			self.rect = self.image.get_rect()
			# print(self.rect)

			#Posicionando o drone na metade da altura tela e menos da metade da largura.
			self.rect[0] = ((400 / 2) - 32) - 100
			self.rect[1] = (600 / 2) - 32


			#Movimento ativo do Drone
			self.speed = SPEED

		def update(self):
			self.current_image = (self.current_image + 1) % 2
			self.image = self.images[ self.current_image ]

			#Fazendo o drone cair com o tempo
			self.rect[1] += self.speed
			self.speed += GRAVITY

		def bump(self):
			self.speed = -SPEED


	class Ground(pygame.sprite.Sprite):
		def __init__(self, xpos):
			pygame.sprite.Sprite.__init__(self)

			self.image = pygame.image.load('img/ground.png').convert_alpha()
			self.image = pygame.transform.scale(self.image,(GROUND_WIDTH,GROUND_HEIGHT))
			self.mask = pygame.mask.from_surface(self.image)

			self.rect = self.image.get_rect()
			#Posicionando o chão no chão.
			self.rect[0] = xpos
			self.rect[1] = (SCREEN_HEIGHT - GROUND_HEIGHT) #Tamanho da tela - altura do objeto.

		def update(self):
			self.rect[0] -= GAME_SPEED

	class Pipe(pygame.sprite.Sprite):

		def __init__(self, inverted,  xpos, ysize):
			pygame.sprite.Sprite.__init__(self)

			self.image = pygame.image.load('img/pipe.png').convert_alpha()
			self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
			self.rect = self.image.get_rect()

			self.rect[0] = xpos

			if inverted:
				self.image = pygame.transform.flip(self.image, False, True)
				self.rect[1] = - (self.rect[3] - ysize)

			else:
				self.rect[1] = SCREEN_HEIGHT - ysize

			self.mask = pygame.mask.from_surface(self.image)


		def update(self):
			self.rect[0] -= GAME_SPEED

	"""
		Funções
	"""
	#Função para testar se o sprite saiu completamente da tela.
	def is_off_screen(sprite):
		return sprite.rect[0] < -(sprite.rect[2]) #rect[2] retorna a largura do sprite.

	#Função para geração de canos aleatórios
	def get_random_pipes(xpos):
		size = random.randint(100, 300)
		pipe = Pipe(False, xpos, size)
		pipe_inverted = Pipe(True, xpos, (SCREEN_HEIGHT - size - random.randint(100, 200)))
		return (pipe, pipe_inverted)

	#If GameOver
	def gameOverText():
		fontOver = pygame.font.Font('freesansbold.ttf', 30)
		fontText = pygame.font.Font('freesansbold.ttf', 18)
		fontFinalScore = pygame.font.Font('freesansbold.ttf', 24)
		overText = fontOver.render('GAME OVER', True, (255, 255, 255) )
		playAgainText = fontText.render('Press Space to play again', True, (255, 255, 255))
		finalScoreText = fontFinalScore.render(str(score_value) + ' Points', True, (255,215,0))
		screen.blit(overText, (100, 150))
		screen.blit(playAgainText, (80, 250))
		screen.blit(finalScoreText, (140, 200))

	#Mostrar pontuação
	score_value = 0
	def showScore():
		fontScore = pygame.font.Font('freesansbold.ttf', 20)
		scoreText = fontScore.render('Score : ' + str(score_value), True, (255, 255, 255) )
		screen.blit(scoreText, (10, 10))


	#Menu
	def showMenu():
		fontMenu = pygame.font.Font('freesansbold.ttf', 24)
		menuText = fontMenu.render('Welcome to Crashing Drone!', True, (255, 255, 255))
		fontStart = pygame.font.Font('freesansbold.ttf', 18)
		startText = fontStart.render('Press Space to start', True, (255, 255, 255))
		screen.blit(menuText, (40, 150))
		screen.blit(startText, (100, 200))

	"""
			Objetos
	"""

	#Criando um background
	background = pygame.image.load('img/background.png')
	#Transformando a imagem no tamanho da tela do jogo.
	background = pygame.transform.scale(background, (400, 500))

	#Criando os personagens
	drone_group = pygame.sprite.Group()
	drone = Drone()
	drone_group.add(drone)

	#Criando o chão

	ground_group = pygame.sprite.Group()
	for i in range(2):
		ground = Ground(GROUND_WIDTH * i)
		ground_group.add(ground)

	#Criando os canos

	pipe_group = pygame.sprite.Group()
	for i in range(2):
		pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
		pipe_group.add(pipes[0])
		pipe_group.add(pipes[1])

	#Criando a música de background
		pygame.mixer.init()


		pygame.mixer.music.load('sound/background.wav')
		pygame.mixer.music.play(-1) #-1 plays on loop

	"""
			Rodando o jogo
	"""
	clock = pygame.time.Clock()
	running = False
	gameOver = False
	menu = True

	while menu:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					menu = False
					running = True

		screen.blit(background,(0,0))
		ground_group.draw(screen)
		drone_group.draw(screen)
		showMenu()
		pygame.display.update()
		

	while running:
		clock.tick(30)
		droneSound = pygame.mixer.Sound('sound/drone.wav')
		pygame.mixer.Sound.set_volume(droneSound, 0.1)
		droneSound.play(-1)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					drone.bump()

	#Rodando os updates da tela
		screen.blit(background,(0,0))

		if is_off_screen(ground_group.sprites()[0]):
			ground_group.remove(ground_group.sprites()[0])
			new_ground = Ground(GROUND_WIDTH - 20)
			ground_group.add(new_ground)

		if is_off_screen(pipe_group.sprites()[0]):
				pipe_group.remove(pipe_group.sprites()[0])
				pipe_group.remove(pipe_group.sprites()[0])
				score_value += 1
				pipes = get_random_pipes(SCREEN_WIDTH * 2)

				pipe_group.add(pipes[0])
				pipe_group.add(pipes[1])

		drone_group.update()
		drone_group.draw(screen)
		pipe_group.update()
		pipe_group.draw(screen)
		ground_group.update()
		ground_group.draw(screen)

		showScore()


		if (pygame.sprite.groupcollide(drone_group, ground_group, False, False, pygame.sprite.collide_mask)) or (pygame.sprite.groupcollide(drone_group, pipe_group, False, False, pygame.sprite.collide_mask)):
			#Game Over
			droneSound.stop()
			explosionSound = mixer.Sound('sound/explosion.wav')
			explosionSound.play()
			pygame.display.update()

			running = False
			gameOver = True

		pygame.display.update()


	while gameOver:
		screen.blit(background,(0,0))
		ground_group.draw(screen)
		gameOverText()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					main()		



		pygame.display.update()

if __name__ == '__main__':
	main()