import os

import torch
import matplotlib
import matplotlib.pyplot as plt

from tqdm.auto import tqdm

matplotlib.style.use('ggplot')


def save_model(model, version: int, epoch: int) -> None:
    """
    Function to save the trained model to disk.
    """
    model_name = f'model_v{version}'
    model_path = os.path.join('..', 'models', model_name)
    os.makedirs(model_path, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(model_path, f"{model_name}_epoch_{epoch+1}.pth"))


def save_plots(train_acc, valid_acc, train_loss, valid_loss, version: int):
    """
    Function to save the loss and accuracy plots to disk.
    """
    model_name = f'model_v{version}'
    model_path = os.path.join('..', 'models', model_name)
    # Accuracy plots.
    plt.figure(figsize=(10, 7))
    plt.plot(
        train_acc, color='green', linestyle='-',
        label='train accuracy'
    )
    plt.plot(
        valid_acc, color='blue', linestyle='-',
        label='validataion accuracy'
    )
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig(f"{model_path}/accuracy.png")

    # Loss plots.
    plt.figure(figsize=(10, 7))
    plt.plot(
        train_loss, color='orange', linestyle='-',
        label='train loss'
    )
    plt.plot(
        valid_loss, color='red', linestyle='-',
        label='validataion loss'
    )
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.savefig(f"{model_path}/loss.png")


def train(
        model,
        trainloader,
        optimizer,
        criterion,
        device='cpu',
        scheduler=None,
        epoch=None
):
    model.train()
    print('Training')
    train_running_loss = 0.0
    train_running_correct = 0
    counter = 0
    iters = len(trainloader)
    for i, data in tqdm(enumerate(trainloader), total=len(trainloader)):
        counter += 1
        image, labels = data
        image = image.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        # Forward pass.
        outputs = model(image)
        # Calculate the loss.
        loss = criterion(outputs, labels)
        train_running_loss += loss.item()
        # Calculate the accuracy.
        _, preds = torch.max(outputs.data, 1)
        train_running_correct += (preds == labels).sum().item()
        # Backpropagation.
        loss.backward()
        # Update the weights.
        optimizer.step()

        if scheduler is not None:
            scheduler.step(epoch + i / iters)

    # Loss and accuracy for the complete epoch.
    epoch_loss = train_running_loss / counter
    epoch_acc = 100. * (train_running_correct / len(trainloader.dataset))
    return epoch_loss, epoch_acc
