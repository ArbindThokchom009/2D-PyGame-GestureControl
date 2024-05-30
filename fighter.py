import pygame

class Fighter():
    def __init__(self,player, x, y, flip, data, sprite_sheet, animation_steps,sound):

        
        self.player = player
        self.size = data[0]
        self.flip = flip
        self.image_scale = data[1]
        self.offset = data[2]
        self.animation_list = self.load_image(sprite_sheet, animation_steps)

        self.action = 0  # to determine the currently doing eg
        # 0 : idle
        # 1 : run
        # 2 : Attack1
        # 3 : attack2
        # 4 : hit
        # 5 : death

        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]

        self.update_time = pygame.time.get_ticks()

        self.rect = pygame.Rect((x, y, 80, 180))  # character

        self.vel_y = 0

        self.running = False  # non running state

        self.jump = False

        self.attacking = False

        self.attack_type = 0
        
        self.attack_cool_down = 0
        
        self.hit = False

        self.health = 100
        self.alive = True
        
        self.attack_sound = sound

    def load_image(self, sprite_sheet, animation_steps):

        # extract image from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x*self.size, y*self.size, self.size, self.size)
                
                temp_img_list.append(pygame.transform.scale(
                    temp_img, (self.size*self.image_scale, self.size*self.image_scale)))
            animation_list.append(temp_img_list)

        return animation_list

    def move(self, screen_width, screen_height, surface, target,round_over):

        SPEED = 10
        GRAVITY = 2

        # dx and dy is delta variable that can be change
        dx = 0
        dy = 0

        self.running = False
        self.attack_type = 0
        # Get keypresses
        key = pygame.key.get_pressed()

        # Can only perform other action if not currently attacking
        if self.attacking == False and self.alive==True and round_over == False:
            
            #check player 1 control
            if self.player==1:
                
                # Movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = +SPEED
                    self.running = True

                # Jumping
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # Attack
                if key[pygame.K_r] or key[pygame.K_t]:

                    self.attack(target)

                    # determined which attack type was used
                    if key[pygame.K_r]:
                        self.attack_type = 1

                    if key[pygame.K_t]:
                        self.attack_type = 2
                        
            #check player 2 control
            if self.player==2:
                
                # Movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = +SPEED
                    self.running = True

                # Jumping
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # Attack
                if key[pygame.K_l] or key[pygame.K_p]:

                    #self.attack(surface, target)
                    self.attack(target)

                    # determined which attack type was used
                    if key[pygame.K_l]:
                        self.attack_type = 1

                    if key[pygame.K_p]:
                        self.attack_type = 2

        # Apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Ensure the player on screen
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left

        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # Ensure player face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # apply attack cooldown
        if self.attack_cool_down > 0:
            self.attack_cool_down -= 1

        # Update player position Rect

        self.rect.x += dx
        self.rect.y += dy

    # Handle animation updates
    def update(self):

        # check what sction the player is performing

        if self.running == True:
            self.update_action(1)  # run
        elif self.jump == True:
            self.update_action(2)  # jump
        elif self.attack_type == 2:
            self.update_action(4)  # attack2
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # attack1
        elif self.hit == True:
            self.update_action(5)  # Hit
        elif self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # death

        else:
            self.update_action(0)  # idle

        animation_cool_down = 50  # in milisecond

        # Update image
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed since the last update
        # current time - that time when first created is greater then 1/2 second is already passed
        if pygame.time.get_ticks() - self.update_time > animation_cool_down:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Check the animation is finish
        if self.frame_index >= len(self.animation_list[self.action]):
            
            # check if the player is death
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cool_down = 20
                # check if the damage was taken
                if self.action == 5:
                    self.hit = False
                    # check if the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cool_down = 20

    #def attack(self, surface, target):
    def attack(self, target):

        if self.attack_cool_down == 0:

            self.attacking = True
            
            self.attack_sound.play()
            
            attacking_rect = pygame.Rect(self.rect.centerx - (
                2 * self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height)

            if attacking_rect.colliderect(target.rect):
                print('hit')
                target.health -= 10
                target.hit = True

            #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        # Check the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(
            img, (self.rect.x-(self.offset[0]*self.image_scale), self.rect.y-(self.offset[1]*self.image_scale)))
