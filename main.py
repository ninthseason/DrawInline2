import interception
import time
import typing
import cv2
from PIL import ImageGrab
import image_edge_detection as ied
import numpy as np
import skimage
from collections import deque
interception.auto_capture_devices()

def move_relative(x: int, y: int):
    interception.move_relative(x, y)
    time.sleep(0.0016)

def continuous_move_relative_manhattan(x: int, y: int):
    while x != 0:
        if x > 0:
            x -= 1
            move_relative(1, 0)
        else:
            x += 1
            move_relative(-1, 0)
    while y != 0:
        if y > 0:
            y -= 1
            move_relative(0, 1)
        else:
            y += 1
            move_relative(0, -1)
    time.sleep(0.1)

def find_first_true(img: np.ndarray):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] == True:
                return [i, j]

def main():
    # time.sleep(5)
    # with interception.hold_mouse("left"):
    #     continuous_move_relative_manhattan(100, 0)
    #     continuous_move_relative_manhattan(0, 100)
    #     continuous_move_relative_manhattan(-100, 0)
    #     continuous_move_relative_manhattan(0, -100)
    img = ImageGrab.grabclipboard()
    if img is None:
        print("No picture in Clipboard.")
    elif isinstance(img, list):
        print("ImageGrab.grabclipboard() return a list[str], but idk why..")
    else:
        edges = typing.cast(cv2.typing.MatLike, ied.canny_edge_detect(img, return_pil=False))
        edges = skimage.morphology.thin(edges)
        tau = [find_first_true(edges)]
        edges[tau[-1][0]][tau[-1][1]] = False # type: ignore
        unfinished_total = True
        while unfinished_total:
            unfinished_local = True
            while unfinished_local:
                origin = typing.cast(list, tau[-1])
                # print(origin)
                if origin[1] + 1 < edges.shape[1] and edges[origin[0]][origin[1] + 1]:  # 下
                    tau.append([origin[0], origin[1] + 1])
                    edges[origin[0]][origin[1] + 1] = False
                elif origin[0] - 1 > -1 and edges[origin[0] - 1][origin[1]]:  # 左
                    tau.append([origin[0] - 1, origin[1]])
                    edges[origin[0] - 1][origin[1]] = False
                elif origin[1] - 1 > -1 and edges[origin[0]][origin[1] - 1]:  # 上
                    tau.append([origin[0], origin[1] - 1])
                    edges[origin[0]][origin[1] - 1] = False
                elif origin[0] + 1 < edges.shape[0] and edges[origin[0] + 1][origin[1]]:  # 右
                    tau.append([origin[0] + 1, origin[1]])
                    edges[origin[0] + 1][origin[1]] = False
                elif origin[0] - 1 > -1 and origin[1] + 1 < edges.shape[1] and edges[origin[0] - 1][origin[1] + 1]:  # 左下
                    tau.append([origin[0] - 1, origin[1] + 1])
                    edges[origin[0] - 1][origin[1] + 1] = False
                elif origin[0] - 1 > -1 and origin[1] - 1 > -1 and edges[origin[0] - 1][origin[1] - 1]:  # 左上
                    tau.append([origin[0] - 1, origin[1] - 1])
                    edges[origin[0] - 1][origin[1] - 1] = False
                elif origin[0] + 1 < edges.shape[0] and origin[1] - 1 > -1 and edges[origin[0] + 1][origin[1] - 1]:  # 右上
                    tau.append([origin[0] + 1, origin[1] - 1])
                    edges[origin[0] + 1][origin[1] - 1] = False
                elif origin[0] + 1 < edges.shape[0] and origin[1] + 1 < edges.shape[1] and edges[origin[0] + 1][origin[1] + 1]:  # 右下
                    tau.append([origin[0] + 1, origin[1] + 1])
                    edges[origin[0] + 1][origin[1] + 1] = False
                else:
                    unfinished_local = False
            origin = typing.cast(list, tau[-1])
            # print(origin)
            visited = np.zeros(shape=[edges.shape[0] + 1, edges.shape[1] + 1])
            visited[-1] = 1
            visited[:, -1] = 1
            visited[origin[0]][origin[1]] = 1
            queue = deque()
            queue.append(origin)
            unfinished_total = False
            # cv2.imwrite("demo.png", edges.view(np.uint8) * 255)
            while len(queue) != 0:
                n = queue.popleft()
                if edges[n[0]][n[1]]:
                    # print(n)
                    tau.append(n)
                    edges[n[0]][n[1]] = False
                    unfinished_total = True
                    break
                if visited[n[0]][n[1] + 1] == 0:
                    queue.append([n[0], n[1] + 1])
                    # edges[n[0]][n[1] + 1] = False
                    visited[n[0]][n[1] + 1] = 1
                if visited[n[0] - 1][n[1] + 1] == 0:
                    queue.append([n[0] - 1, n[1] + 1])
                    # edges[n[0] - 1][n[1] + 1] = False
                    visited[n[0] - 1][n[1] + 1] = 1
                if visited[n[0] - 1][n[1]] == 0:
                    queue.append([n[0] - 1, n[1]])
                    # edges[n[0] - 1][n[1]] = False
                    visited[n[0] - 1][n[1]] = 1
                if visited[n[0] - 1][n[1] - 1] == 0:
                    queue.append([n[0] - 1, n[1] - 1])
                    # edges[n[0] - 1][n[1] - 1] = False
                    visited[n[0] - 1][n[1] - 1] = 1
                if visited[n[0]][n[1] - 1] == 0:
                    queue.append([n[0], n[1] - 1])
                    # edges[n[0]][n[1] - 1] = False
                    visited[n[0]][n[1] - 1] = 1
                if visited[n[0] + 1][n[1] - 1] == 0:
                    queue.append([n[0] + 1, n[1] - 1])
                    # edges[n[0] + 1][n[1] - 1] = False
                    visited[n[0] + 1][n[1] - 1] = 1
                if visited[n[0] + 1][n[1]] == 0:
                    queue.append([n[0] + 1, n[1]])
                    # edges[n[0] + 1][n[1]] = False
                    visited[n[0] + 1][n[1]] = 1
                if visited[n[0] + 1][n[1] + 1] == 0:
                    queue.append([n[0] + 1, n[1] + 1])
                    # edges[n[0] + 1][n[1] + 1] = False
                    visited[n[0] + 1][n[1] + 1] = 1

        tau_diff = []
        # print(tau)
        for i in range(len(tau) - 1):
            a = tau[len(tau) - 2 - i] 
            b = tau[len(tau) - 1 - i]
            tau_diff.append([b[1] - a[1], b[0] - a[0]])  # type: ignore
        tau_diff.reverse()
        # print(tau_diff)

        interception.mouse_down("left")
        for i in tau_diff:
            if -1 <= i[0] <= 1 and -1 <= i[1] <= 1:
                move_relative(i[0], i[1])
                time.sleep(0.01)
            else:
                # print("jump to", i[0], i[1])
                interception.mouse_up("left")
                time.sleep(0.5)
                continuous_move_relative_manhattan(i[0], i[1])
                time.sleep(0.1)
                interception.mouse_down("left")
                time.sleep(0.1)
                
        interception.mouse_up("left")
        

if __name__ == "__main__":
    main()
