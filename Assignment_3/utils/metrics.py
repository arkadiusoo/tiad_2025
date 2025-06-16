import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
import numpy as np

def evaluate_model(model, val_gen, figure=None):
    y_true = val_gen.classes
    y_pred_probs = model.predict(val_gen)
    y_pred = (y_pred_probs > 0.5).astype(int)

    report_text = classification_report(y_true, y_pred, target_names=val_gen.class_indices.keys(), output_dict=True)

    plot_confusion_matrix(y_true, y_pred, val_gen.class_indices, figure=figure)
    plot_roc_curve(y_true, y_pred_probs, figure=figure)

    return report_text

def plot_confusion_matrix(y_true, y_pred, labels_dict, figure=None):
    fig = figure if figure is not None else plt.figure()
    ax = fig.add_subplot(121 if figure else 111)
    cm = confusion_matrix(y_true, y_pred)
    im = ax.imshow(cm, cmap="Blues")
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    fig.colorbar(im, ax=ax)
    tick_marks = np.arange(len(labels_dict))
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(labels_dict.keys())
    ax.set_yticks(tick_marks)
    ax.set_yticklabels(labels_dict.keys())

def plot_roc_curve(y_true, y_probs, figure=None):
    fig = figure if figure is not None else plt.figure()
    ax = fig.add_subplot(122 if figure else 111)
    fpr, tpr, _ = roc_curve(y_true, y_probs)
    roc_auc = auc(fpr, tpr)
    ax.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})")
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend(loc="lower right")
