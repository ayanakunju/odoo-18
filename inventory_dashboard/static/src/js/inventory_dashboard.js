/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
import { Component, onWillStart, useEffect, useState } from  "@odoo/owl";
const actionRegistry = registry.category("actions");

class InventoryDashboard extends Component {
    setup() {
         super.setup()
         this.orm = useService('orm')

    onWillStart(async () => {
//              this.isStockManager = await user.hasGroup("stock.group_stock_manager");
              this._inventory_data()
        });

    useEffect(() => {
        });
    }
    async _inventory_data() {
           var self = this;
//           const admin = this.isStockManager
           this.orm.call("stock.picking", "get_inventory_tiles_data", [], {}).then((result) => {
           console.log(result)
           document.getElementById('stock_incoming').append(result.stock_incoming);
           document.getElementById('stock_outgoing').append(result.stock_outgoing);
           document.getElementById('stock_internal').append(result.stock_internal);
        });
    }
}
InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("inventory_dashboard_tag", InventoryDashboard);
