/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
import { Component, onWillStart, useEffect, useState, useRef } from  "@odoo/owl";
const actionRegistry = registry.category("actions");

class InventoryDashboard extends Component {
    setup() {
        super.setup()
        this.orm = useService('orm')
        this.barRef = useRef('data_bar')
        this.pieRef = useRef('data_pie')
        this.doughnutRef = useRef('data_doughnut')
        this.lineRef = useRef('data_line')

        this.state = useState({
                 fetch_data: {},
                 location_data: {},
                });

        this.barChart = null;
        this.pieChart = null;
        this.doughnutChart = null;
        this.lineChart = null;
//        this.selected_time_period = false


        onWillStart(async () => {
//                  this.isStockManager = await user.hasGroup("stock.group_stock_manager");
                  this._inventory_fetch_tile_data()
                  this. _storage_location_table()
            });


        this._location_data_pie()
        this._product_average_expense_bar()
        this._stock_valuation_doughnut_chart()
        this._product_move_line_chart()

    }


    async _inventory_fetch_tile_data() {
           const admin = this.isStockManager
//           var self = this;
//           var time = selected_period;
           this.orm.call("stock.picking", "get_inventory_tiles_data", [admin], {}).then((result) => {
               this.state.fetch_data = result
               console.log('rrrr',this.state.fetch_data)
           });
    }

    async _location_data_pie(){
        this.orm.call("stock.move", "get_stock_move_location", []).then( (result) => {
            var name = result.name
            var count = result.count;
            var ctx = this.pieRef.el.id
            if (this.pieChart){
                this.pieChart.destroy();
            }
            this.pieChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: name,
                    datasets: [{
                        label: 'Count',
                        data: count,
                        barThickness: 10,
                        type: 'pie',
                        fill: false
                    }]
                },
            });
        });
    }

    async _product_average_expense_bar() {
        this.orm.call("stock.picking", "get_product_average_expense", []).then((result) => {
            var product_names = Object.keys(result);
            var average_price = Object.values(result)
            var ctx = this.barRef.el.id
            if (this.barChart){
            this.barChart.destroy();
            }
            this.barChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: product_names,
                datasets: [{
                    label: product_names,
                    backgroundColor: [
                                    "#003f5c","#2f4b7c","#f95d6a","#665191",
                                    "#d45087","#ff7c43","#ffa600","#a05195",
                                    "#6d5c16","#CCCCFF"
                                ],
                    data: average_price
                }]
            },
            options: {}
              });
        })
       }

    async _stock_valuation_doughnut_chart(){
        this.orm.call("stock.valuation.layer", "get_stock_value", []).then( (result) => {
            var product_names = result.name;
            var stock_value = result.stock_value;
            var ctx = this.doughnutRef.el.id
            if (this.doughnutChart){
            this.doughnutChart.destroy();
            }
            this.doughnutChart = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: product_names,
                datasets: [{
                    backgroundColor: [
                                   "#665191","#a05195",
                                    "#CCCCFF","#ffa600","#a05195",
                                    "#6d5c16","#CCCCFF"
                                ],
                    data: stock_value
                }]
               },
              });
             });
        }

    async _storage_location_table(){
        await this.orm.call("stock.picking", "get_locations",[]
        ).then((result) => {
            this.state.location_data = result
            console.log('dataaa',this.state.location_data)
            });
    }

    async _product_move_line_chart(){
        this.orm.call("stock.move.line", "get_product_moves",[]).then( (result) => {
            var product_names = result.name;
            var move_count = result.count;
            var ctx = this.lineRef.el.id
            if (this.lineChart){
            this.lineChart.destroy();
            }
            this.lineChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: product_names,
                datasets: [{
                    label: 'Product Move',
                    backgroundColor: [
                                    "#ff7c43","#2f4b7c","#a05195","#665191",
                                    "#d45087","#ff7c43","#ffa600","#a05195",
                                    "#6d5c16","#CCCCFF"
                                ],
                    data: move_count
                }]
              },
            });
        });
    }

    redirectToIncoming(){
    this.env.services.action.doAction({
         type: 'ir.actions.act_window',
         name: 'Outgoing',
         res_model: 'stock.picking',
         views: [[false, "list"], [false, "form"]],
         target: 'current',
        domain : [['picking_type_id.code', '=','incoming'],
                  ['state', 'not in',['done', 'cancel']]]
       });
 }

    redirectToOutgoing(){
    this.env.services.action.doAction({
         type: 'ir.actions.act_window',
         name: 'Outgoing',
         res_model: 'stock.picking',
         views: [[false, "list"], [false, "form"]],
         target: 'current',
        domain : [['picking_type_id.code', '=','outgoing'],
                  ['state', 'not in',['done', 'cancel']]]
       });
 }

    redirectToInternalTransfer(){
    this.env.services.action.doAction({
         type: 'ir.actions.act_window',
         name: 'Internal Transfer',
         res_model: 'stock.picking',
         views: [[false, "list"], [false, "form"]],
         target: 'current',
        domain : [['picking_type_id.code', '=','internal'],
                  ['state', 'not in',['done', 'cancel']]]
       });
 }

}
InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("inventory_dashboard_tag", InventoryDashboard);
