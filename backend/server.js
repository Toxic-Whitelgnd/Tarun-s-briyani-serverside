const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(bodyParser.json());


mongo_url = "mongodb+srv://whitelegend56:odLPpZbJETcnzrWg@restaurant.lgfalwj.mongodb.net/tarunsbriyani"

mongoose.connect(mongo_url,{ useNewUrlParser: true, useUnifiedTopology: true });

const db1 = mongoose.connection;
db1.on('error',console.error.bind(console,'connection error'));
db1.once('open',()=>{
    console.log("Connected to mongodb");
})


const db = mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'1234',
    database:'tarun_briyani'

})



app.get('/inprogress',(req,res) => {
    const query1 = "select * from order_tracking where status ='Your order is in prepration';";

    db.query(query1,(err,data)=>{
        if(err) return res.json(err);
        return res.json(data)
    })
});


app.get('/dispatchorder',(req, res)=>{
    const q = "select * from order_tracking where status = 'Your order is ready yet to dispatch';";

    db.query(q,(err,data)=>{
        if(err) return res.json(err);
        return res.json(data)
    })
    
});

app.get('/onthewayorder',(req, res)=>{
    const q = "select * from order_tracking where status = 'Your order is out for delivery';";

    db.query(q,(err,data)=>{
        if(err) return res.json(err);
        return res.json(data)
    })
    
});

app.get('/get-deliverdorder',(req, res)=>{
    const q = "select * from order_tracking where status = 'your order has been delivered successfully';";

    db.query(q,(err,data)=>{
        if(err) return res.json(err);
        return res.json(data)
    })
    
});

app.post('/update-orders',(req,res) => {
    let{order_id,status} = req.body;
    console.log(order_id,status);

    // db query 
    
    const q = "update order_tracking set status = '"+status+"' where order_id = '"+order_id+"' ";

    db.query(q,(err,data)=>{
        if(err) return res.json(err);
    })

    return res.json({"message":"success"})
});

// MONGODB QUERIES
const ordertrackschema = new mongoose.Schema({
    order_id: {
        type: String,
        required: true
    },
    status: {
        type: String,
        required: true
    },
},{strict:false});
const ordertrack = mongoose.model('ordertrack',ordertrackschema,'order_tracking');

app.get('/progress-order',async (req,res)=>{

    var progreesorder = await ordertrack.find({"status":"Your order is in progress"})
    // console.log(progreesorder);
    return res.json(progreesorder)
});

app.get('/dispatch-order',async (req,res)=>{
    var dispatchorder = await ordertrack.find({"status":"Your order has been dispatched "});
    console.log(dispatchorder);
    return res.json(dispatchorder);
});

app.get('/on-the-way-order',async (req,res)=>{
    var onthewayorder = await ordertrack.find({"status":"Your order is out for delivery"});
    console.log(onthewayorder);
    return res.json(onthewayorder);
});

app.get("/get-delivered-order",async (req,res)=>{
    var deliveredorder = await ordertrack.find({"status":"your order has been delivered successfully"});
    console.log(deliveredorder);
    return res.json(deliveredorder);
});

app.post("/update-order-req",async (req,res)=>{
    let{order_id,status} = req.body;
    console.log(typeof(order_id),status);
    var msg = "success";

    try {
        var check =await ordertrack.updateMany(
            {
                order_id:order_id,
            },
            {
                $set:{
                    status:status,
                }
            },
            { new: true },
        );
        console.log(check);
        
    } catch (error) {
        console.log("Error updating order");
        msg = "error"
    }finally {
        // Close the Mongoose connection after the update operation
        // mongoose.connection.close();
    }
    

    return res.json({"message":msg});
});



app.get('/',(req,res)=>{
    res.json("Server for Tarun's Briyani paradise ");
}
);

app.listen(9999,()=>{
    console.log("listening on port:http://localhost:9999");
})