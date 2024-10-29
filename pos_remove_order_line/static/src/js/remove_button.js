/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(ControlButtons.prototype, {
    async onClick() {
        var order = this.pos.get_order();
        var lines = order.get_orderlines();
        if (lines.length != 0) {
            lines.filter(line => line.get_product())
                .forEach(line => order.removeOrderline(line));
        }else {
            this.notification.add(("No Items to remove."), { type: "danger" });
        }
    }
});
