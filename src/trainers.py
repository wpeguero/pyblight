"""Set of Classes for Training Machine Learning Models."""
import torch
from torch import nn, optim
from torch.utils import data

with open('src/model_version.txt', 'r') as fp:
    VERSION = int(fp.read())
    fp.close()


class Trainer:
    """Base class for training machine learning models."""

    def __init__(self, model:nn.Module, optimizer:optim.Optimizer, loss):
        """Initialize the class."""
        self.model = model
        self.opt = optimizer
        self.criterion = loss

    def get_model(self):
        """Get the model post training.

        Returns
        -------
        torch Module
            The model at any point in time before or after training.
        """
        return self.model

    def train(self, trainloader:data.DataLoader, epochs:int, gpu=False):
        """Train the machine learning model.

        Uses the given model, optimizer, and loss provided when the
        class was initizalized in conjunction with the trainloader to
        train the given model. The model is trained based on the
        number of epochs provided. For each epoch, the model is
        trained by iterating through the dataset and the model
        weights are updated based on the loss.

        Parameters
        ----------
        trainloader : torch DataLoader
            dataset loaded and ready for model training.

        epochs : int
            number of times the model loops through the batched set.

        gpu : bool
            Determines whether the gpu is used to train dataset.
        """
        if  gpu == True:
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        else:
            device = torch.device("cpu")
        print("The model will be running on ", device, "device")
        self.model.to(device)
        steps_per_epoch = len(trainloader.dataset) // trainloader.batch_size
        print("Starting Training of {} version {}.".format(self.model.__class__.__name__, VERSION))
        for epoch in range(epochs):
            running_loss = 0.0
            self.model.train(True)
            train_step(self. epoch, trainloader)

    def train_step(self, epoch:int, trainloader:data.DataLoader):
        """Single Step for training model."""
        raise NotImplementedError("method train_step must be implemented.")


class ClassTrainer(Trainer):
    """Class for training pytorch machine learning classifiers.

    This class functions as an environment for training the
    pytorch models.

    Parameters
    ----------
    model : torch Module
        Model which will be trained within this class.
    optimizer : torch Optimizer
        optimizer used to change the weights on the machine
        learning model.
    loss : torch Loss
        The chosen loss to compare the prediction and the target.
    """

    def __init__(self, model:nn.Module, optimizer:optim.Optimizer, loss):
        """Initialize the class."""
        self.model = model
        self.opt = optimizer
        self.criterion = loss

    def train_step(self, epoch:int, trainloader:data.DataLoader):
        correct = 0
        total = 0
        for i, (inputs, labels) in enumerate(trainloader, 0):
            inputs = inputs.to(device)
            labels = labels.to(device)
            self.opt.zero_grad()

            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.opt.step()

            _, ipredicted = torch.max(outputs.data, 1)
            _, lindices = torch.max(labels.data, 1)
            total += labels.size(0)
            correct += (ipredicted == lindices).sum().item()
            running_loss += loss.item()
        print(f'[{epoch + 1:3d}/{epochs}] loss: {running_loss / steps_per_epoch:.3f}, accuracy: {round(100 * correct / total, 2)}')
            correct = 0
            total = 0
            for i, (inputs, labels) in enumerate(trainloader, 0):
                inputs = inputs.to(device)
                labels = labels.to(device)
                self.opt.zero_grad()

                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.opt.step()

                #_, ipredicted = torch.max(outputs.data, 1)
                ipredicted= outputs.max(1).indices
                #_, lindices = torch.max(labels.data, 1)
                lindices = labels.max(1).indices
                total += labels.size(0)
                correct += (ipredicted == lindices).sum().item()
                running_loss += loss.item()
            print(f'[{epoch + 1:3d}/{epochs}] loss: {running_loss / steps_per_epoch:.3f}, accuracy: {round(100 * correct / total, 2)}')

    @staticmethod
    def test(model, testloader:data.DataLoader, classes:tuple, gpu:bool=False, version:int=0):
        """Test the model's ability to classify on a never before seen dataset.

        Parameters
        ----------
        testloader : pytorch DataLoader
            Dataset that was never seen by the model.
        classes : tuple
            An immutable list of classes from the dataset.
        gpu : bool
            Determines whether to send the model and data to the gpu
            or the cpu.
        """
        if  gpu == True:
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        else:
            device = torch.device("cpu")
        model.to(device)
        correct_pred = {classname: 0 for classname in classes}
        total_pred = {classname: 0 for classname in classes}
        results = list("Accuracy Results on test set for Machine Learning Model {}\n".format(model.__class__.__name__))

        with torch.no_grad():
            for images, labels in testloader:
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)
                _, predictions = torch.max(outputs, 1)
                _, lindices = torch.max(labels, 1)
                for label, pred in zip(lindices, predictions):
                    if label == pred:
                        correct_pred[classes[label]] += 1
                    total_pred[classes[label]] += 1
        for classname, correct_count in correct_pred.items():
            accuracy = 100 * float(correct_count) / total_pred[classname]
            results.append(f'Accuracy for class: {classname:5s} is {accuracy:.1f}%\n')
            print(f'Accuracy for class: {classname:5s} is {accuracy:.1f}%')
        with open('data/{}_results_version_{}.txt'.format(model.__class__.__name__, version), 'w') as fp:
            fp.writelines(results)
            fp.close()

    @staticmethod
    def create_confusion_matrix(preds, labels, device):
        """
        Create a confusion matrix for calculating metrics.

        Creates a Tensor that can be used to develop metrics, such as
        accuracy, precision, etc.

        Parameters
        ----------
        preds
            The predicted values
        labels
            The true value
        """
        n_classes = len(labels[0])
        cm = torch.zeros(n_classes, n_classes)
        cm.to(device)
        pindices = preds.max(1).indices
        pindices.to(device)
        lindices = labels.max(1).indices
        lindices.to(device)
        for l, p in zip(lindices, pindices):
            cm[p, l] += 1
        return cm
