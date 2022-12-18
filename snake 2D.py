from tkinter import  * 
from PIL import Image, ImageTk
import random


Movechange = 20
move_pre_second =10
Game_speed = 1500 // move_pre_second




class Snake(Canvas):
	def __init__(self):
		super().__init__(width = 600, height = 620,  background ='black', highlightthickness = 0)

		self.reset= [(100,100),(80,100),(60,100)]
		self.snake_positions = [(100,100),(80,100),(60,100)]
		self.food_positions = self.set_new_food_position()
		self.score = 0
		self.loop = None
		self.directoin ='d'

		self.bind_all('<Key>', self.on_key_press)
		#เช็คตลอด ว่ากดkeyอะไรบ้าง เมือมีการกดจะแสดงself.on_key_press
		self.bind('<F1>',self.rungame)

		self.load_assets()
		self.create_objects()
		self.rungame()
		self.starting = True



	def load_assets(self):
		self.snake_body_image = Image.open('./assets/body.png')
		self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

		self.food_image = Image.open('./assets/food.png')
		self.food = ImageTk.PhotoImage(self.food_image)

		self.BGG_image = Image.open('./assets/555.png')
		self.BGG = ImageTk.PhotoImage(self.BGG_image)

	def create_objects(self):

		self.create_image(300,320,image = self.BGG )
		#create score
		Font = (None,14)
		self.create_text(45,12,text ='Score:  {}'.format(self.score),tag = 'score',fill='#FFF',font=Font)

		#crate body
		for x_pos , y_pos in self.snake_positions:
			self.create_image ( x_pos,y_pos,image = self.snake_body ,tag = 'snake')


		#createe food
		self.create_image(self.food_positions[0],self.food_positions[1],image = self.food,tag='food')# *self.food   
		#createe rctanglee เส้นกรอบ	
		self.create_rectangle(7,27,593,613,outline = "#FFF")

	def move_snake(self):


		head_x , head_y = self.snake_positions[0]

		if self.directoin == 'd':
			new_head_pos = (head_x + Movechange, head_y)	
		#new_head_pos = (head_x + Movechange, head_y)
		elif self.directoin =='a':
			new_head_pos = (head_x - Movechange, head_y)
		elif self.directoin == 'w':
			new_head_pos = (head_x, head_y - Movechange)
		elif self.directoin == 's':
			new_head_pos =(head_x,head_y + Movechange)

		self.snake_positions = [new_head_pos] + self.snake_positions[:-1]#ลบตัวท้ายออก

		findsnake = self.find_withtag('snake')
		for segment, pos in zip(findsnake,self.snake_positions):
			#[(segment),(120,100)),(segment),(120,100)),(segment),(120,100))]
			self.coords(segment,pos)

	def rungame(self):

		if self.check_collisions() and self.starting == True:
			self.after_cancel(self.loop)
			self.starting =False
			self.delete('all')
			self.create_text(300,300,justify = CENTER,
							text=f'GAME OVER\n\nScore: {self.score}\n\nNew Game <F1>',fill="#FFF",font=(None,30))

		elif self.check_collisions() and self.starting == False:
			self.delete('all')
			self.snake_positions = self.reset
			self.food_positions = self.set_new_food_position()
			self.create_objects()
			self.starting = True
			self.directoin = 'd'
			self.score = 0
			self.loop = self.after(Game_speed,self.rungame)

		else:	
			self.check_food_collisions()
			self.move_snake()
			self.loop = self.after(Game_speed,self.rungame) #loop game

	def on_key_press(self,e):
		new_directoin = e.keysym #key press

		all_directoin = ('w','s','a','d')
		opposites = ({'w','s'},{'a','d'})

		if (new_directoin in all_directoin and {new_directoin,self.directoin} not in opposites ) :
			self.directoin = new_directoin
		elif new_directoin == 'F1':
			self.rungame()

		print("KEY:",self.directoin)

	def check_collisions(self):
		head_x , head_y = self.snake_positions[0]
		return (head_x in (0,600) or head_y in (20,620) or (head_x,head_y) in self.snake_positions[1:]) 

	def check_food_collisions(self):
		if self.snake_positions[0] == self.food_positions:
			self.score += 1
			self.snake_positions.append(self.snake_positions[-1])

			self.create_image( * self.snake_positions[-1],image = self.snake_body, tag='snake')

			score = self.find_withtag('score')
			self.itemconfigure(score,text ='Score: {}'.format(self.score),tag = 'score' )
	
			self.food_positions = self.set_new_food_position()
			self.coords(self.find_withtag('food'),self.food_positions)
	
	def set_new_food_position(self):
		while True:
			x_pos =random.randint(1,29)* Movechange
			y_pos =random.randint(3,30)* Movechange
			food_positions = (x_pos,y_pos)
			if food_positions not in self.snake_positions:
				return food_positions


GUI = Tk()
GUI.title('SNAKE2D')
GUI.resizable(False,False)

game = Snake()
game.pack()

GUI.mainloop()
