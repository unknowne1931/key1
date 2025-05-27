const express = require("express")
const mongoose = require("mongoose")
const cors = require("cors")
const app = express()

app.use(express.json())
app.use(cors())
app.use(express.urlencoded({ extended: true }))
app.use(express.static("public"))

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
    next();
});

const mongoURI = "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
mongoose.connect(mongoURI,)
.then(() => console.log('MongoDB connected'))
.catch(err => console.log(err));


app.get("/", (req, res) => {
    res.send("Hello World!")
})


const Question_Data_base_Schema = new mongoose.Schema({
    question : {
        type: String,
        required: true
    },
    answer : {
        type: String,
        required: true
    },  
    a : {
        type: String,
        required: true
    },
    
    b : {
        type: String,
        required: true
    },
    
    c : {
        type: String,
        required: true
    },

    d : {
        type: String,
        required: true
    },

    language : {
        type: String,
        required: true
    },

    category : {
        type: String,
        required: true
    },  
    difficulty : {
        type: String,
        required: true
    },
    type : {
        type: String,
        required: true
    },

    image : {
        type: String,
        required: false
    },

    seconds : {
        type: Number,
        required: true
    },

}, { timestamps: true });

const QuestionModule = mongoose.model('Question Data', Question_Data_base_Schema);


app.post("/api/question", async (req, res) => {
    const { question, answer, a, b, c, d, language, category, difficulty, type, image, seconds } = req.body

    try {
        const newQuestion = new QuestionModule({
            question,
            answer,
            a,
            b,
            c,
            d,
            language,
            category,
            difficulty,
            type,
            image,
            seconds
        })

        await newQuestion.save()
        res.status(200).json({ message: "Question added successfully", status : "OK" })
    } catch (error) {
        console.error(error)
        res.status(500).json({ message: "Error adding question" })
    }
})  


app.get("/api/question", async (req, res) => {  
    try {
        const questions = await QuestionModule.find()
        res.status(200).json(questions)
    } catch (error) {
        console.error(error)
        res.status(500).json({ message: "Error fetching questions" })
    }
}
)

app.get("/api/questions/length", async (req, res) => {
    try {
        const count = await QuestionModule.countDocuments()
        res.status(200).json({ count })
    } catch (error) {
        console.error(error)
        res.status(500).json({ message: "Error fetching question count" })
    }
}
)

app.delete("/api/question/:id", async (req, res) => {
    const { id } = req.params

    try {
        await QuestionModule.findByIdAndDelete(id)
        res.status(200).json({ message: "Question deleted successfully" })
    } catch (error) {
        console.error(error)
        res.status(500).json({ message: "Error deleting question" })
    }
})  

app.put("/api/question/:id", async (req, res) => {
    const { id } = req.params
    const { question, answer, a, b, c, d, language, category, difficulty, type, image, seconds } = req.body

    try {
        await QuestionModule.findByIdAndUpdate(id, {
            question,
            answer,
            a,
            b,
            c,
            d,
            language,
            category,
            difficulty,
            type,
            image,
            seconds
        })
        res.status(200).json({ message: "Question updated successfully" })
    } catch (error) {
        console.error(error)
        res.status(500).json({ message: "Error updating question" })
    }
})


app.listen(80, () => {
    console.log("Server is running on port 80")
})



