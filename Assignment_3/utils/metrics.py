import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
import numpy as np

def evaluate_model(model, val_gen):
    y_true = val_gen.classes
    y_pred_probs = model.predict(val_gen)
    y_pred = (y_pred_probs > 0.5).astype(int)

    print(classification_report(y_true, y_pred, target_names=val_gen.class_indices.keys()))

    plot_confusion_matrix(y_true, y_pred, val_gen.class_indices)
    plot_roc_curve(y_true, y_pred_probs)

def plot_confusion_matrix(y_true, y_pred, labels_dict):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure()
    plt.imshow(cm, cmap="Blues")
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.colorbar()
    tick_marks = np.arange(len(labels_dict))
    plt.xticks(tick_marks, labels_dict.keys())
    plt.yticks(tick_marks, labels_dict.keys())
    plt.show()

def plot_roc_curve(y_true, y_probs):
    fpr, tpr, _ = roc_curve(y_true, y_probs)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.show()
