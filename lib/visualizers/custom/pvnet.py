# from lib.datasets.dataset_catalog import DatasetCatalog
# from lib.config import cfg
# import pycocotools.coco as coco
# import numpy as np
# from lib.utils.pvnet import pvnet_config
# import matplotlib.pyplot as plt
# from lib.utils import img_utils
# import matplotlib.patches as patches
# from lib.utils.pvnet import pvnet_pose_utils


# mean = pvnet_config.mean
# std = pvnet_config.std


# class Visualizer:

#     def __init__(self):
#         args = DatasetCatalog.get(cfg.test.dataset)
#         self.ann_file = args['ann_file']
#         self.coco = coco.COCO(self.ann_file)

#     def visualize(self, output, batch):
#         inp = img_utils.unnormalize_img(batch['inp'][0], mean, std).permute(1, 2, 0)
#         kpt_2d = output['kpt_2d'][0].detach().cpu().numpy()

#         img_id = int(batch['img_id'][0])
#         anno = self.coco.loadAnns(self.coco.getAnnIds(imgIds=img_id))[0]
#         kpt_3d = np.concatenate([anno['fps_3d'], [anno['center_3d']]], axis=0)
#         K = np.array(anno['K'])

#         pose_gt = np.array(anno['pose'])
#         pose_pred = pvnet_pose_utils.pnp(kpt_3d, kpt_2d, K)

#         corner_3d = np.array(anno['corner_3d'])
#         corner_2d_gt = pvnet_pose_utils.project(corner_3d, K, pose_gt)
#         corner_2d_pred = pvnet_pose_utils.project(corner_3d, K, pose_pred)

#         fig, ax = plt.subplots(1, figsize=(14, 10))
#         ax.imshow(inp)
#         ax.add_patch(patches.Polygon(xy=corner_2d_gt[[0, 1, 3, 2, 0, 4, 6, 2]], fill=False, linewidth=1, edgecolor='g'))
#         ax.add_patch(patches.Polygon(xy=corner_2d_gt[[5, 4, 6, 7, 5, 1, 3, 7]], fill=False, linewidth=1, edgecolor='g'))
#         ax.add_patch(patches.Polygon(xy=corner_2d_pred[[0, 1, 3, 2, 0, 4, 6, 2]], fill=False, linewidth=1, edgecolor='b'))
#         ax.add_patch(patches.Polygon(xy=corner_2d_pred[[5, 4, 6, 7, 5, 1, 3, 7]], fill=False, linewidth=1, edgecolor='b'))
#         plt.show()

#     def visualize_train(self, output, batch):
#         inp = img_utils.unnormalize_img(batch['inp'][0], mean, std).permute(1, 2, 0)
#         mask = batch['mask'][0].detach().cpu().numpy()
#         vertex = batch['vertex'][0][0].detach().cpu().numpy()
#         img_id = int(batch['img_id'][0])
#         anno = self.coco.loadAnns(self.coco.getAnnIds(imgIds=img_id))[0]
#         fps_2d = np.array(anno['fps_2d'])
#         plt.figure(0)
#         plt.subplot(221)
#         plt.imshow(inp)
#         plt.subplot(222)
#         plt.imshow(mask)
#         plt.plot(fps_2d[:, 0], fps_2d[:, 1])
#         plt.subplot(224)
#         plt.imshow(vertex)
#         plt.savefig('test.jpg')
#         plt.close(0)




from lib.datasets.dataset_catalog import DatasetCatalog
from lib.config import cfg
import pycocotools.coco as coco
import numpy as np
from lib.utils.pvnet import pvnet_config
import matplotlib.pyplot as plt
from lib.utils import img_utils
import matplotlib.patches as patches
from lib.utils.pvnet import pvnet_pose_utils

mean = pvnet_config.mean
std = pvnet_config.std

class Visualizer:

    def __init__(self):
        args = DatasetCatalog.get(cfg.test.dataset)
        self.ann_file = args['ann_file']
        self.coco = coco.COCO(self.ann_file)

    def visualize(self, output, batch):
        inp = img_utils.unnormalize_img(batch['inp'][0], mean, std).permute(1, 2, 0)
        kpt_2d = output['kpt_2d'][0].detach().cpu().numpy()

        img_id = int(batch['img_id'][0])
        anno = self.coco.loadAnns(self.coco.getAnnIds(imgIds=img_id))[0]
        kpt_3d = np.concatenate([anno['fps_3d'], [anno['center_3d']]], axis=0)
        K = np.array(anno['K'])

        pose_gt = np.array(anno['pose'])
        pose_pred = pvnet_pose_utils.pnp(kpt_3d, kpt_2d, K)

        corner_3d = np.array(anno['corner_3d'])
        corner_2d_gt = pvnet_pose_utils.project(corner_3d, K, pose_gt)
        corner_2d_pred = pvnet_pose_utils.project(corner_3d, K, pose_pred)

        fig, ax = plt.subplots(1, figsize=(14, 10))
        ax.imshow(inp)
        ax.add_patch(patches.Polygon(xy=corner_2d_gt[[0, 1, 3, 2, 0, 4, 6, 2]], fill=False, linewidth=2, edgecolor='lime'))
        ax.add_patch(patches.Polygon(xy=corner_2d_gt[[5, 4, 6, 7, 5, 1, 3, 7]], fill=False, linewidth=2, edgecolor='lime'))
        ax.add_patch(patches.Polygon(xy=corner_2d_pred[[0, 1, 3, 2, 0, 4, 6, 2]], fill=False, linewidth=2, edgecolor='r'))
        ax.add_patch(patches.Polygon(xy=corner_2d_pred[[5, 4, 6, 7, 5, 1, 3, 7]], fill=False, linewidth=2, edgecolor='r'))

        # def draw_axes(center_3d, pose, color):
        #     axis_length = 1  # Adjust axis length if necessary
        #     axes_3d = np.array([[axis_length, 0, 0], [0, axis_length, 0], [0, 0, axis_length]])  # Length of the axes
        #     axes_3d_transformed = (pose[:3, :3] @ axes_3d.T).T + center_3d
        #     axes_2d = pvnet_pose_utils.project(np.vstack((center_3d, axes_3d_transformed)), K, pose)

        #     ax.plot([axes_2d[0, 0], axes_2d[1, 0]], [axes_2d[0, 1], axes_2d[1, 1]], color=color[0], linewidth=2)  # X axis
        #     ax.plot([axes_2d[0, 0], axes_2d[2, 0]], [axes_2d[0, 1], axes_2d[2, 1]], color=color[1], linewidth=2)  # Y axis
        #     ax.plot([axes_2d[0, 0], axes_2d[3, 0]], [axes_2d[0, 1], axes_2d[3, 1]], color=color[2], linewidth=2)  # Z axis

        # # Draw ground truth axes
        # center_3d_gt = np.array(anno['center_3d']).reshape(1, -1)
        # draw_axes(center_3d_gt, pose_gt, ['r', 'g', 'b'])

        # # Draw predicted axes
        # center_3d_pred = center_3d_gt  # Use the same center for prediction
        # draw_axes(center_3d_pred, pose_pred, ['r', 'g', 'b'])

        plt.show()

    def visualize_train(self, output, batch):
        inp = img_utils.unnormalize_img(batch['inp'][0], mean, std).permute(1, 2, 0)
        mask = batch['mask'][0].detach().cpu().numpy()
        vertex = batch['vertex'][0][0].detach().cpu().numpy()
        img_id = int(batch['img_id'][0])
        anno = self.coco.loadAnns(self.coco.getAnnIds(imgIds=img_id))[0]
        fps_2d = np.array(anno['fps_2d'])
        plt.figure(0)
        plt.subplot(221)
        plt.imshow(inp)
        plt.subplot(222)
        plt.imshow(mask)
        plt.plot(fps_2d[:, 0], fps_2d[:, 1])
        plt.subplot(224)
        plt.imshow(vertex)
        plt.savefig('test.jpg')
        plt.close(0)
