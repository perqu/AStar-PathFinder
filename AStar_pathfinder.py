import pygame
import math
import db,vis
from queue import PriorityQueue

def diagonal_distance(current_cell, goal):
	x1, y1 = current_cell
	x2, y2 = goal
	dx = abs(x1 - x2)
	dy = abs(y1 - y2)
	return dx + dy + (math.sqrt(2) - 2) * min(dx, dy)

def algorithm(draw, grid, start, end):
	open_set = PriorityQueue()
	open_set.put((0, start))
	came_from = {}
	g_score = {point: float("inf") for row in grid for point in row}
	g_score[start] = 0
	f_score = {point: float("inf") for row in grid for point in row}
	f_score[start] = diagonal_distance(start.get_pos(), end.get_pos())

	possible_points = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		current = open_set.get()[1]
		possible_points.remove(current)
		current.update_neighbors(grid)

		if current == end:
			vis.reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			if neighbor.is_closed() == False:
				tentative_g_score = g_score[current] + diagonal_distance(current.get_pos(), neighbor.get_pos())
				if tentative_g_score < g_score[neighbor]:
					came_from[neighbor] = current
					g_score[neighbor] = tentative_g_score
					f_score[neighbor] = tentative_g_score + diagonal_distance(neighbor.get_pos(), end.get_pos())
					if neighbor not in possible_points:
						open_set.put((f_score[neighbor], neighbor))
						possible_points.add(neighbor)
						if neighbor.is_end() == False: neighbor.make_open()
		draw()

		if current != start:
			current.make_closed()

	return False

def main():
	grid = vis.make_grid(db.ROWS)

	start = None
	end = None

	running = True
	while running:
		vis.draw(grid, db.ROWS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = vis.get_clicked_pos(pos)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = vis.get_clicked_pos(pos)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					algorithm(lambda: vis.draw(grid, db.ROWS), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = vis.make_grid(db.ROWS)
					
	pygame.quit()

main()