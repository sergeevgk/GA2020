package epc.dialogs;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.DialogWrapper;
import org.jetbrains.annotations.Nullable;

public abstract class EpcDialog extends DialogWrapper {

    protected EpcDialog(@Nullable Project project) {
        super(project);
    }

    public void showDialog() {
        init();
        show();
    }

    public void waitForInput() {
        if (super.isOK()) {
            return;
        }
        System.out.println("cancelled");
    }
}
