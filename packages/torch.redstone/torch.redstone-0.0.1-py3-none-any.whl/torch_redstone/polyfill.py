import torch


class Polyfill:
    @staticmethod
    def cdist2(src: torch.Tensor, dst: torch.Tensor):
        """
        Computes batched the squared 2-norm distance between each pair of the two collections of row vectors.
        src (Tensor): input tensor of shape [B, N, C].
        dst (Tensor): input tensor of shape [B, M, C].
        Output: per-point square distance of shape [B, N, M].
        """
        B, M, _ = dst.shape
        dist = torch.baddbmm(torch.sum(src ** 2, -1, keepdim=True), src, dst.permute(0, 2, 1), alpha=-2)
        dist += torch.sum(dst ** 2, -1).view(B, 1, M)
        return dist

    @staticmethod
    def cdist(src: torch.Tensor, dst: torch.Tensor):
        """
        Computes batched the 2-norm distance between each pair of the two collections of row vectors.
        src (Tensor): input tensor of shape [B, N, C].
        dst (Tensor): input tensor of shape [B, M, C].
        Output: per-point distance of shape [B, N, M].
        """
        return Polyfill.cdist2(src, dst).sqrt_()

    @staticmethod
    def square(x: torch.Tensor):
        return x * x

    @staticmethod
    def broadcast_to(tensor: torch.Tensor, shape):
        return tensor.expand(shape)


if not hasattr(torch, 'square'):
    torch.square = Polyfill.square

if not hasattr(torch, 'broadcast_to'):
    torch.broadcast_to = Polyfill.broadcast_to

if not hasattr(torch, 'cdist'):
    torch.cdist = Polyfill.cdist
