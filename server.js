const express = require('express');
const app = express();
const mongoose = require('mongoose');
const cluster = require("cluster");
// const compression = require("compression");
// app.use(compression());


const mongoURI = "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
mongoose.connect(mongoURI,)
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log(err));

const port = 80

app.listen(port || 80, () => {
    console.log(`server started port ${port}`)
})



process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection:', reason);
});




const QnoSchema = new mongoose.Schema({
    Time: String,
    user: String,
    img: String,
    Questio: String,
    qno: String,
    a: String,
    b: String,
    c: String,
    d: String,
    Ans: String,
    lang: String,
    tough: String,
    seconds: String,
    sub_lang: {
        default: "",
        type: String
    },

    yes: {
        default: "",
        type: []
    },
    no: {
        default: "",
        type: []
    }

}, { timestamps: true });

const QuestionModule = mongoose.model('Qno_Count', QnoSchema);


const AllLanguagesSchema = new mongoose.Schema({
    Time: { type: Date, default: Date.now },  // Use Date for Time field
    lang: [{ type: String }]  // Define lang as an array of strings
}, { timestamps: true });

const AllLanguagemodule = mongoose.model('All_Languages', AllLanguagesSchema);

app.get("/all/lang/data", async (req, res)=>{
    try{
        const data = await AllLanguagemodule.findOne({})
        if(!data){
            return res.status(400).json({message :"Data not found"})
        }
        return res.status(200).json({data : data.lang})
    }catch (error) {
        console.error(error);
        return res.status(500).json({ message: "Internal Server Error" });
    }
})



//change tough from users Answerd
app.get("/get/questions/from/qno/:lang", async (req, res) => {
    try {
        const { lang } = req.params;

        // Fetch all questions matching the given language
        const questions = await QuestionModule.find({ lang });

        if (!questions.length) {
            return res.status(404).json({ message: "No questions found for this language" });
        }

        let updatedQuestions = [];

        for (const question of questions) {
            if (!question || !question.tough) {
                continue; // Skip if the question is null or doesn't have a toughness level
            }

            const yesCount = question.yes?.length || 0;
            const noCount = question.no?.length || 0;
            let newTough = question.tough;

            if (yesCount > noCount) {
                if (!["Easy", "Too Easy"].includes(question.tough)) {
                    newTough = "Easy";
                }
            } 
            else if (yesCount === noCount) {
                if ((question.yes.length)-1 === 0 && (question.no.length)-1 === 0){
                    
                }else{
                    if (question.tough !== "Medium") {
                        newTough = "Medium";
                    }
                }
                
            } 
            else {
                if (!["Tough", "Too Tough"].includes(question.tough)) {
                    newTough = "Tough";
                }
            }

            if (newTough !== question.tough) {
                question.tough = newTough;
                await question.save();
                // console.log(`Updated qno: ${question.qno}, New tough: ${newTough}`);
                updatedQuestions.push({ qno: question.qno, newTough });
            }
        }

        return res.status(200).json({ message: "Processed all questions", updatedQuestions });

    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: "Internal Server Error" });
    }
});

// //Balance the Questions from Easy, Medium, tough
// app.get("/balance/all/questions/from/easy/medium/tough/:lang", async (req, res) => {
//     const { lang } = req.params;

//     try {
//         // Fetch questions by difficulty level
//         const too_easy = await QuestionModule.find({ lang, tough: "Too Easy" });
//         const easy = await QuestionModule.find({ lang, tough: "Easy" });
//         const medium = await QuestionModule.find({ lang, tough: "Medium" });
//         const tough = await QuestionModule.find({ lang, tough: "Tough" });
//         const too_tough = await QuestionModule.find({ lang, tough: "Too Tough" });

//         // Find total questions in each category
//         const too_easy_len = too_easy.length;
//         const easy_len = easy.length;
//         const medium_len = medium.length;
//         const tough_len = tough.length;
//         const too_tough_len = too_tough.length;

//         // Total number of questions
//         const total_questions = too_easy_len + easy_len + medium_len + tough_len + too_tough_len;

//         // Function to shuffle an array
//         const shuffleArray = (array) => array.sort(() => Math.random() - 0.5);

//         // Shuffle all categories
//         shuffleArray(too_easy);
//         shuffleArray(easy);
//         shuffleArray(medium);
//         shuffleArray(tough);
//         shuffleArray(too_tough);

//         // Distribute questions in a balanced way
//         const groups = [];
//         let index = 0;

//         while (index < total_questions) {
//             let group = [];

//             if (too_easy.length) group.push(too_easy.pop());
//             if (easy.length) group.push(easy.pop());
//             if (medium.length) group.push(medium.pop());
//             if (tough.length) group.push(tough.pop());
//             if (too_tough.length) group.push(too_tough.pop());

//             // If we still need more questions to reach 10, fill from available categories
//             while (group.length < 10) {
//                 if (too_easy.length) group.push(too_easy.pop());
//                 else if (easy.length) group.push(easy.pop());
//                 else if (medium.length) group.push(medium.pop());
//                 else if (tough.length) group.push(tough.pop());
//                 else if (too_tough.length) group.push(too_tough.pop());
//                 else break; // Stop if no more questions available
//             }

//             groups.push(group);
//             index += 10;
//         }

//         return res.status(200).json({
//             message: "Balanced questions grouped successfully",
//             total_questions,
//             groups
//         });

//     } catch (error) {
//         console.error(error);
//         return res.status(500).json({ message: "Internal Server Error" });
//     }
// });




app.get("/balance/all/questions/from/easy/medium/tough/:lang", async (req, res) => {
    const { lang } = req.params;

    try {
        // Fetch all questions grouped by difficulty
        let too_easy = await QuestionModule.find({ lang, tough: "Too Easy" });
        let easy = await QuestionModule.find({ lang, tough: "Easy" });
        let medium = await QuestionModule.find({ lang, tough: "Medium" });
        let tough = await QuestionModule.find({ lang, tough: "Tough" });
        let too_tough = await QuestionModule.find({ lang, tough: "Too Tough" });

        // Combine all questions
        let all_questions = [...too_easy, ...easy, ...medium, ...tough, ...too_tough];
        let total_questions = all_questions.length;

        if (total_questions === 0) {
            return res.status(404).json({ message: "No questions available for this language" });
        }

        // Shuffle questions randomly
        const shuffleArray = (array) => array.sort(() => Math.random() - 0.5);
        shuffleArray(all_questions);

        // Assign new qno values and update in DB
        let bulkUpdates = [];
        for (let i = 0; i < total_questions; i++) {
            bulkUpdates.push({
                updateOne: {
                    filter: { _id: all_questions[i]._id }, // Find the specific question
                    update: { $set: { qno: i + 1 } } // Update qno sequentially
                }
            });
        }

        // Execute bulk update in MongoDB
        await QuestionModule.bulkWrite(bulkUpdates);

        // Fetch updated questions to verify the new order
        const updatedQuestions = await QuestionModule.find({ lang }).sort({ qno: 1 });

        return res.status(200).json({
            message: "Updated question numbers successfully",
            total_questions,
            questions: updatedQuestions
        });

    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: "Internal Server Error" });
    }
});





app.get("/balance/all/questions/from/easy/medium/tough/02/:lang", async (req, res) => {
    const { lang } = req.params;

    try {
        // Fetch all questions grouped by difficulty
        let too_easy = await QuestionModule.find({ lang, tough: "Too Easy" });
        let easy = await QuestionModule.find({ lang, tough: "Easy" });
        let medium = await QuestionModule.find({ lang, tough: "Medium" });
        let tough = await QuestionModule.find({ lang, tough: "Tough" });
        let too_tough = await QuestionModule.find({ lang, tough: "Too Tough" });

        // Combine all questions
        let all_questions = [...too_easy, ...easy, ...medium, ...tough, ...too_tough];
        let total_questions = all_questions.length;

        if (total_questions === 0) {
            return res.status(404).json({ message: "No questions available for this language" });
        }

        // Shuffle questions randomly
        const shuffleArray = (array) => array.sort(() => Math.random() - 0.5);
        shuffleArray(all_questions);

        // Assign new qno values and update in DB
        let bulkUpdates = [];
        for (let i = 0; i < total_questions; i++) {
            bulkUpdates.push({
                updateOne: {
                    filter: { _id: all_questions[i]._id }, // Find the specific question
                    update: { $set: { qno: i + 1 } } // Update qno sequentially
                }
            });
        }

        // Execute bulk update in MongoDB
        await QuestionModule.bulkWrite(bulkUpdates);

        // Fetch updated questions to verify the new order
        const updatedQuestions = await QuestionModule.find({ lang }).sort({ qno: 1 });

        // for()

        return res.status(200).json({
            message: "Updated question numbers successfully",
            total_questions,
            questions: updatedQuestions
        });

    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: "Internal Server Error" });
    }
});


app.get("/all/:lang", async (req, res) => {
    try {
        const { lang } = req.params;
        const data = await QuestionModule.find({ lang }).lean();

        let Data = [];

        for (let i = 1; i < data.length; i++) {
            const dat = await QuestionModule.findOne({ qno: i, lang }).lean(); // Await the query
            if (dat) {
                const list_dat = {
                    Qno : dat.qno,
                    Tough : dat.tough
                }
                Data.push(list_dat); // Store the `tough` field in the array
            }
        }

        return res.status(200).json({ Data });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: "Internal Server Error" });
    }
});
