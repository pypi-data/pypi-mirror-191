from random import randint, randrange
import random
import string


#  @author Satyajit319 <satyajit319@gmail.com>
#  date 27/03/2022

firstMaleName = ['Hari', 'sam', 'Mukund', 'Nabaghan', 'Abhishek', 'Suresh', 'Santunu', 'Akashya', 'Haribol',
                 'Madhab', 'Balkrushna', 'Aarav', 'Vihaan', 'Vivaan', 'Ananya', 'Diya', 'Advik', 'Kabir', 'Anaya',
                 'Aarav', 'Vivaan', 'Aditya', 'Vivaan', 'Vihaan', 'Arjun', 'Vivaan', 'Reyansh', 'Mohammed', 'Sai',
                 'Arnav', 'Aayan', 'Krishna', 'Ishaan', 'Shaurya', 'Atharva', 'Advik', 'Pranav', 'Advaith', 'Aaryan',
                 'Dhruv', 'Kabir', 'Ritvik', 'Aarush', 'Kian', 'Darsh', 'Veer', 'Aadil', 'Aakash', 'Aarif',
                 'Aashu', 'Aatif', 'Aayush', 'Abdul', 'Abdullah', 'Abhash', 'Abhimanyu', 'Abhinav', 'Abhishek', 'Abrar',
                 'Adi', 'Aditya', 'Aftab', 'Agyapad', 'Ahsan', 'Ajay', 'Ajeet', 'Ajit', 'Ajman', 'Akash',
                 'Akbar', 'Akhilesh', 'Akhtar', 'Akram', 'Akshay', 'Akshpaat', 'Altaf', 'Aman', 'Amar', 'Amarjeet',
                 'Ameen', 'Amil', 'Amit', 'Anil', 'Anjali', 'Ankit', 'Ankur', 'Ansh', 'Anshu', 'Anshul',
                 'Ansu', 'Anuj', 'Anup', 'Anurag', 'Anwari', 'Aoosaf', 'Arif', 'Arman', 'Arsad',
                 'Arsh', 'Arun', 'Arvind', 'Aryan', 'Ashish', 'Ashok', 'Ashu', 'Ashutosh', 'Asif', 'Atul',
                 'Avinash', 'Ayan', 'Azam', 'Bablu', 'Babu', 'Babulal', 'Baksi', 'Balbir', 'Balram', 'Balwant',
                 'Banarsi', 'Bandu', 'Bangali', 'Banwari', 'Barkat', 'Begraj', 'Bhagwans', 'Bhajanlal', 'Bhanu',
                 'Bharma', 'Bhupender', 'Bhupesh', 'Bijender', 'Bijendra', 'Bikki', 'Birender', 'Birij', 'Birjesh', 'Bishan',
                 'Bittu', 'Bobi', 'Boby', 'Bram', 'Brijmohan', 'Chandan', 'Chander', 'Chanderpal', 'Chandra', 'Chandrram',
                 'Chatan', 'Chatar', 'Chaterpal', 'Cheddi', 'Chetan', 'Chetanram', 'Chirag', 'Chitrangans', 'Chran', 'Daler',
                 'Daniel', 'Danish', 'Daya', 'Deep', 'Deepak', 'Deepchand', 'Deepender', 'Deewan', 'Desh',
                 'Deshraj', 'Deva', 'Devender', 'Devinder', 'Devraj', 'Dhalchand', 'Dhanna', 'Dharam', 'Dharmandra', 'Dharmender',
                 'Dharmvir', 'Dheeraj', 'Dhramender', 'Dhrmveer', 'Dilip', 'Dinesh', 'Divansh', 'Divyansh', 'Dular', 'Durganand',
                 'Faijal', 'Farid', 'Farmaan', 'Firoj', 'Fulmiya', 'Ganesh', 'Gaurav', 'Gauri', 'Gautam', 'Ghan',
                 'Ghanshyam', 'Giri', 'Girish', 'Gopi', 'Gorav', 'Gourav', 'Gulfam', 'Gulreg', 'Gulshan', 'Gyanendra',
                 'Haider', 'Hansraj', 'Harak', 'Hararat', 'Harendra', 'Hari', 'Harish', 'Harison', 'Harkesh', 'Harpal',
                 'Harsh', 'Harshal', 'Harvinder', 'Hazrat', 'Hemant', 'Himanshu', 'Hosiyarilal', 'Hrithik', 'Imran', 'Inder',
                 'Inderjeet', 'Irshad', 'Ishan', 'Ishant', 'Ishwar', 'Islam', 'Jabbar', 'Jabir', 'Jagmal', 'Jahagir',
                 'Jahid', 'Jaiprakash', 'Jasbir', 'Jasveer', 'Jatin', 'Javed', 'Jeeshan', 'Jeetu', 'Jeeya', 'Jitender',
                 'Jitendera', 'Jitendra', 'Kabul', 'Kaif', 'Kalu', 'Kamruddin', 'Kanhaiya', 'Kapil',
                 'Karan', 'Kavilash', 'Keshave', 'Khemraj', 'Khursheed', 'Kiran', 'Kishan', 'Kripal', 'Krishan', 'Krishana',
                 'Kuldeep', 'Kumar', 'Kumari', 'Kunal', 'Kundan', 'Kushal', 'Laksh', 'Lal', 'Lalan', 'Lalaram',
                 'Lalit', 'Lamani', 'Lave', 'Lawrence', 'Laxman', 'Lekhraj', 'Leo', 'Loknath', 'Lokesh',
                 'Madan', 'Mahaveer', 'Mahender', 'Mahendra', 'Mahesh', 'Mahipal', 'Mamchand', 'Mamta', 'Man', 'Manful',
                 'Manish', 'Manjeet', 'Manjiv', 'Mannu', 'Manoj', 'Manpreet', 'Mithlesh', 'Mobin', 'Mohan', 'Mohit',
                 'Moni', 'Monu', 'Mukeemuddin', 'Mukesh', 'Muneer', 'Munesh', 'Nadeem', 'Nandkishore', 'Nandmeena', 'Nandu',
                 'Nanhe', 'Narayan', 'Narender', 'Naresh', 'Naseem', 'Nashim', 'Neeraj', 'Nikhil', 'Nitin', 'Noorhasan',
                 'Omprakash', 'Pancu', 'Pankaj', 'Paras', 'Pardeep', 'Parmod', 'Parteek', 'Partik', 'Pavan', 'Pawan',
                 'Phooleshwar', 'Pintu', 'Piyush', 'Pooja', 'Prabhjeet', 'Pradeep', 'Prahlad', 'Pramod', 'Prasant', 'Praveen',
                 'Prem', 'Prhalad', 'Prince', 'Punarjyoti', 'Punit', 'Pushkar', 'Puspak', 'Rada', 'Radha', 'Radhey',
                 'Raghubir', 'Raghunandan', 'Raghuvir', 'Rahish', 'Rahul', 'Raj', 'Raja', 'Rajan', 'Rajaram', 'Rajeev',
                 'Rajendar', 'Rajender', 'Rajesh', 'Rajiv', 'Rajkumar', 'Rajneesh', 'Rajni', 'Raju', 'Rajveer', 'Rakesh',
                 'Ram', 'Ramchander', 'Ramesh', 'Ramhetu', 'Ramkishan', 'Ramprasad', 'Ramtek', 'Randhir', 'Ranjeet', 'Ranjit',
                 'Raseel', 'Ratiman', 'Ravi', 'Ravikant', 'Ravinder', 'Ravindra', 'Raviraj', 'Ridhakaran', 'Rihan', 'Rinki',
                 'Rinku', 'Rishi', 'Riyaz', 'Robin', 'Rohit', 'Ronak', 'Roshan', 'Rupender', 'Rupesh', 'Sachin',
                 'Saddam', 'Sahil', 'Sahrukh', 'Sajjan', 'Salim', 'Salin', 'Salmaan', 'Same', 'Sameem', 'Sameer',
                 'Samsuddin', 'Sandeep', 'Sanjay', 'Sanjeev', 'Sanjiv', 'Sanni', 'Sanny', 'Santosh', 'Sartaj', 'Sarvan',
                 'Satbar', 'Satender', 'Satish', 'Satpal', 'Satyam', 'Satyvrat', 'Saurabh', 'Sehzad', 'Shabuddin', 'Shagufta',
                 'Shail', 'Shailesh', 'Shakil', 'Shakti', 'Shambhu', 'Shamim', 'Shankar', 'Sharukh', 'Shashank', 'Shashikant',
                 'Shaukat', 'Shayam', 'Shayamveer', 'Shibu', 'Shisupal', 'Shiv', 'Shiva', 'Shivam', 'Shivyalam', 'Shobharam',
                 'Shripal', 'Shubham', 'Shyam', 'Shyamlal', 'Shyamveer', 'Sidharath', 'Sivam', 'Somnath', 'Sonu',
                 'Subhakar', 'Subhas', 'Subhash', 'Sudhansu', 'Sudhir', 'Suhail', 'Sujeet'
                 ]
title = ["Sahu", "Behera", "Nayak", "Das", "Pradhan", "Naik", "Majhi", "Jena", "Malik",
         "Swain", "Patra", "Barik", "Mohanty", "Raut", "Bhoi", "Panda", "Sahoo", "Sethy", "Dei",
         "Biswal", "Singh", "Parida", "Munda", "Mahanta", "Mahapatra", "Samal", "Mishra", "Maharana",
         "Rana", "Dash", "Bag", "Dehuri", "Padhan", "Meher", "Gaud", "Pradhana", "Bibi", "Muduli", "Harijan",
         "Shabar", "Sethi", "Jani", "Nag", "Mandal", "Murmu", "Patel", "Rout", "Mallick", "Gauda", "Bhue",
         "Kisan", "Nahak", "Giri", "Pattnayak", "Panigrahi", "Senapati", "Padhi", "Khan", "Bhatara", "Bariha",
         "Dalei", "Bewa", "Lenka", "Bhatra", "Bhuyan", "Mahakud", "Dalai", "Oram", "Ganda", "Suna", "Ray", "Tudu",
         "Gouda", "Pujari", "Tripathi", "Simha", "Ojha", "Kar", "Kumbhar", "Nath", "Nanda", "Sa", "Rath", "Seth",
         "Mohanta", "Dhal", "Mahananda", "Mahalik", "Marndi", "Soren", "Palei", "Baral", "Digal", "Hemrum",
         "Prushti", "Tandi", "Pati", "Bagha", "Dharua", "Khatua", "Bindhani", "Raul", "Pal", "Bagartti", "Kahanra",
         "Putel", "Bisoyi", "Sabar", "Kandi", "Mohapatra", "Shatapathi", "Dakua", "Samantaray", "Khuntia", "Mallik",
         "Santa", "Mirdha", "Khara", "Acharya", "Bisoi", "Begum", "Dip", "Mali", "Pani", "Rao", "Sing", "Gochhayat",
         "Guru", "Agrawal", "Hansdah", "Bal", "Chowdhury", "Khatun", "Hembram", "Pande", "Bisi", "Chhatria", "Sharma",
         "Debi", "Khadia", "Hati", "Dora", "Rautray", "Ghadei", "Mahakur", "Kujur", "Ekka", "Lakra", "Podh", "Mukhi",
         "Khil", "Kumar", "Hantal", "Tarai", "Dehury", "Gahir", "Rait", "Dey", "Saren", "Khamari", "Pattnaik", "Pangi",
         "Ho", "Jal", "Banachhor", "Gamanga", "Alli", "Hota", "Sunani", "Hansa", "Pallai", "Sutar", "Sahani", "Naek",
         "Badatya", "Saha", "Khilar", "Dalabehera", "Dandasena", "Paik", "Pujhari", "Pradhani", "Redi", "Pattanayak",
         "Purtti", "Gond", "Nial", "Bhol", "Mahanti", "Subudhi", "Shadangi", "Biswas", "Madakami", "Kisku", "Paraja",
         "Gadanayak", "Kuanra", "Tripathy", "Barla", "Chanda", "Ghosh", "Bhanja", "Barad", "Rohidas", "Thakur", "Mangaraj",
         "Gadaba", "Chalan", "Datta", "Marandi", "Kalo", "Gupta", "Hansda", "Goud", "Mahakul", "Jhankar", "Ghadai",
         "Beura", "Minz", "Juanga", "Bhumia", "Paikaray", "Sarakar", "Prusty", "Sasamal", "Lohar", "Minja", "Misra",
         "Puhan", "Tanti", "Bagh", "Satanami", "Amanatya", "Thapa", "Lakada", "Behura", "Kadraka", "Budek", "Deo",
         "Kamar", "Moharana", "Kishan", "Dhurua", "Lugun", "Samanta", "Sandh", "Mahanandia", "Kanhar", "Gopal",
         "Beshra", "Badaik", "Luha", "Prasad", "Tirkey", "Tirki", "Mundari", "Bibhar", "Chandan", "Padiami",
         "Bhutia", "Sabat", "Bastia", "Bhoe", "Jhodia", "Raita", "Jagat", "Malla", "Chhatar", "Mahankud", "Baske", "Kata",
         "Badhei", "Danasana", "Mahali", "Satapathy", "Kaanra", "Madi", "Toppo", "Choudhury", "Kharsel", "Bej", "Raj",
         "Durga", "Nandi", "Kanda", "Sisa", "Deheri", "Karmi", "Sen", "Maiti", "Hikaka", "Bishoyi", "Karan", "Purohit",
         "Tappo", "Samad", "Tiria", "Mahar", "Shandh", "Dandapat", "Dalapati", "Pattanaik", "Rama", "Sagar", "Danga",
         "Pingua", "Bhatta", "Kerketta", "Muni", "Kalar", "Mahanty", "Palai", "Debata", "Martha", "Devi", "Tarei",
         "Begam", "Set", "Adhikari", "Agrawalla", "Mantri", "Karnna", "Hial", "Bhati", "Reddy", "Mandangi", "Bhukta",
         "Dhir", "Chhura", "Bidika", "Dungdung", "Parija", "Kabasi", "Kabi", "Mahammad", "Sai", "Tete", "Chatar",
         "Mahala", "Dungadunga", "Durua", "Kumura", "Kulu", "Badi", "Gagarai", "Baliyarasinh", "Hasada", "Mahana",
         "Karua", "Penthei", "Jain", "Mahakhud", "Khatei", "Parichha", "Haladar", "Bemal", "Birua", "Kerketa",
         "Sarangi", "Disari", "Samarath", "Punji", "Bachha", "Lima", "Bhumij", "Huika", "Roul", "Gadatia", "Amat",
         "Takri", "Bishi", "Paridaa", "Keraketa", "Saura", "Patro", "Tandia", "Samantara", "Thela", "Sial", "Polei",
         "Surin", "Si", "Padhiari", "Polai", "Pod", "Jayapuria", "Bai", "Pasayat", "Behuria", "Harapal", "Bhakta",
         "Pramanik", "Tadingi", "Bera", "Kamila", "Dwibedi", "Khanda", "Karji", "Purty", "Achari", "Parmanik", "Haripal",
         "Kandulana", "Kalet", "Chinda", "Harichandan", "Jagadala", "Bhainsa", "Prusti", "Bihari", "Patnaik", "Tapno", "Golari",
         "Sundaray", "Manahira", "Yadab", "Praharaj", "Jali", "Chhotaray", "Kundu", "Bhokta", "Jojo", "Kharasel", "Kumari",
         "Ghibhela", "Pandit", "Ranasingh", "Mistri", "Gochhaet", "Alam", "Mahato", "Matari", "Jana", "Sinku", "Brahma",
         "Gardia", "Bage", "Bharati", "Taria", "Pahan", "Hansadah", "Bano", "Mahunta", "Padhy", "Randhari", "Routray", "Amanta",
         "Deep", "Khandei", "Kandagari", "Kathar", "Guntha", "Ketaki", "Lahajal", "Nisa", "Miniaka", "Parabhue", "Minyaka",
         "Kunda", "Khandual", "Kindo", "Hembrum", "Palaka", "Kahanr", "Chandi", "Halaba", "Krisani", "Tapo", "Puta", "Buda",
         "Bada", "Sagaria", "Chhatoi", "Gudia", "Baskey", "Negi", "Thanapati", "Sin", "Beg", "Lakshmi", "Saraph", "Gadatya",
         "Sika", "Sarddar", "Luhura", "Patamajhi", "Panaka", "Madhei", "Bariki", "Mahalinga", "Soreng", "Babu", "Saunta",
         "Raju", "Gochhi", "Bishoi", "Choudhuri", "Dhangadamajhi", "Basantia", "Rajahansa", "Dibya", "Sodi", "Shrichandan",
         "Samantaraya", "Tanty", "Champia", "Bhaisal", "Bentakar", "Manna", "Kirsani", "Kudei", "Badajena", "Kalata", "Banara",
         "Parua", "Himirika", "Khemundu", "Danta", "Gantayat", "Josi", "Karuan", "Satapathi", "Sidar", "Kuanr", "Shankhua",
         "Dutta", "Kullu", "Eka", "Luhar", "Bud", "Khura", "Baghar", "Meleka", "Khosala", "Muli", "Kuladip", "Gahan", "Apat",
         "Pandey", "Ram", "Adabar", "Pothal", "Bharasagar", "Dikshit", "Sarenga", "Galari", "Sardar", "Gop", "Raika", "Ganta",
         "Kaibartta", "Kaudi", "Deuri", "Bagar", "Banua", "Bhadra", "Kanta", "Keut", "Shadhangi", "Jadab", "Ksheti", "Bandichhor",
         "Balabantaray", "Tiwari", "Mahat", "Sathua", "Pratihari", "Lohara", "Bardhan", "Xalxo", "Praska", "Bairagi", "Dila",
         "Husen", "Saraka", "Kaur", "Dhibar", "Dixit", "Mandinga", "Mandingi", "Gamango", "Saradar", "Paharia", "Hernna",
         "Tigga", "Bar", "Pagal", "Dhar", "Mandi", "Neti", "Sau", "Padhihari", "Bala", "Patri", "Khalakho", "Dhrua", "Barua",
         "Pruseth", "Badarait", "Yadav", "Bhujabal", "Selama", "Mohakud", "Manika", "Yena", "Pidikaka", "Sukla", "Bagarti", "Chakra",
         "Hosen", "Banka", "Kalasae", "Jued", "Uddin", "Budhia", "Khatoi", "Raya", "Madkami", "Debanath", "Agarwal", "Topno", "Pandab",
         "Hans", "Shandha", "Barge", "Upadhyay", "Kabat", "Baidya", "Parabhoe", "Sith", "Jha", "Benia", "Badara", "Sinha",
         "Sihna", "Pasaet", "Parabhoi", "Champati", "Laguri", "Gemel", "Bhainsal", "Chhanda", "Makar", "Xess", "Adha", "Besra",
         "Chhuria", "Kalandi", "Parwin", "Dandia", "Manasinh", "Kanungoo", "Burudi", "Bahadur", "Sarap", "Santara", "Bagal",
         "Madhi", "Garada", "Ansari", "Nachika", "Khakha", "Garadia", "Mitra", "Sabitri", "Bari", "Chakrabarty", "Dangua",
         "Kandulna", "Dwari", "Bir", "Dhada", "Duria", "Bahidar", "Parbati", "Rajak", "Chowhan", "Kheti", "Tunga", "Karakaria",
         "Kido", "Khila", "Paital", "Pahi", "Ghibela", "Burma", "Khatoon", "Raheman", "Sundara", "Penthoi", "Mahal", "Sandha",
         "Marei", "Rauta", "Pattayat", "Karjee", "Muna", "Juadi", "Pidika", "Majumdar", "Jamuda", "Kulesika", "Pinga", "Jati",
         "Panigrahy", "Patika", "Sendh", "Rautaraya", "Mahabhoi", "Kampa", "Marnni", "Dalua", "Parween", "Lahar", "Deogam",
         "Ranabida", "Karmakar", "Sagria", "Badra", "Besan", "Soni", "Ghasi", "Ali", "Urma", "Singha", "Khosla", "Bhosagar",
         "Saraswati", "Karna", "Khes", "Mugri", "Ranajit", "Jethi", "Agasti", "Shatapathy", "Soy", "Aehmad", "Bara", "Bishayi", "Bishai", "Goswami",
         "Mashra", "Mahankuda", "Parimanik", "Karali", "Pandi", "Bhengra", "Beriha", "Rautaray", "Dal", "Kanungo", "Puala", "Bhagat", "Perei",
         "Baliarasinh", "Pan", "Thatoi", "Urlaka", "Baa", "Karyi", "Dhali", "Baitharu", "Samantasinhar", "Khanam", "Muthamajhi", "Bandichhod",
         "Nathasharma", "Mahamad", "Bahalia", "Hansada", "Jayasinh", "Jerai", "Roy", "Shagadia", "Muria", "Gain", "Barman", "Kalia", "Pushti",
         "Badamundi", "Kusulia", "Lahara", "Sarkar", "Biswakarma", "Baliarasin", "Kandh", "Sah", "Chaudhuri", "Kiro", "Misal", "Peda",
         "Sirika", "Jagadeb", "Guin", "Sidu", "Behara", "Garia", "Sana", "Modi", "Bilunga", "Satpathy", "Suar", "Adajuad", "Sikaka", "Suren", "Matia",
         ]
emlDomain = ['gmail.com', 'yahoo.com', 'hotmail.com', 'rediffmail.com',
             'mns.com', 'github.com', 'bandu.com', 'baidu.com', 'aol.com', 'comcast.net']
upiDomain = ['@BARODAMPAY', '@rbl', '@idbi', '@upi', '@aubank', '@axisbank', '@bandhan', '@dlb', '@indus', '@kbl', '@federal', '@sbi', '@uco',
             '@yesbank', '@citi', '@citigold', '@dlb', '@dbs', '@freecharge', '@okhdfcbank', '@okaxis', '@oksbi', '@okicici', '@hsbc',
             '@idbi', '@icici', '@indianbank', '@allbank', '@kotak', '@ikwik', '@paytm', '@ybl', '@axl', '@ibl', '@sib']
gender = ['Male', 'Female', 'TransGender']
hairColor = ['Black', 'Brown', 'Red', 'Blond']
skinColor = ['Ivory', 'Beige', 'Alabaster', 'Honey', 'Carotenoid', 'Tan', 'Caramel', 'Bronze', 'Mahogany', 'Chestnut', 'Buff', 'Peaches',
             'Umber', 'Praline', 'Espresso Brown', 'Porcelain', 'Hickory', 'Mustard', 'Sable', 'Almond', 'Bisque', 'Teak', 'Cacao', 'Pecan', 'Saddle Brown']
bloodGroup = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
eyeColor = ['Brown', 'Blue', 'Hazel', 'Amber', 'Green', 'Gray', 'Red']
stateName = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
             'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
stateDist = {
    'Andhra Pradesh': ['Anantapuram', 'Chittoor', 'East Godavari', 'Guntur', 'YSR Kadapa', 'Krishna', 'Kurnool', 'Prakasam', 'Sri Potti Sriramulu Nellore', 'Srikakulam', 'Visakhapatnam', 'Vizianagaram', 'West Godavari'],
    'Arunachal Pradesh': ['Anjaw', 'Changlang', 'Dibang Valley', 'East Kameng', 'East Siang', 'Kamle', 'Kra Daadi', 'Kurung Kumey', 'Lepa Rada', 'Lohit', 'Longding', 'Lower Dibang Valley', 'Lower Siang', 'Lower Subansiri', 'Namsai', 'Pakke Kessang', 'Papum Pare', 'Shi Yomi', 'Siang', 'Tawang', 'Tirap', 'Upper Siang', 'Upper Subansiri', 'West Kameng', 'West Siang'],
    'Assam': ['Baksa', 'Barpeta', 'Biswanath', 'Bongaigaon', 'Cachar', 'Charaideo', 'Chirang', 'Darrang', 'Dhemaji', 'Dhubri', 'Dibrugarh', 'Dima Hasao', 'Goalpara', 'Golaghat', 'Hailakandi', 'Hojai', 'Jorhat', 'Kamrup', 'Kamrup Metropolitan', 'Karbi Anglong', 'Karimganj', 'Kokrajhar', 'Lakhimpur', 'Majuli', 'Morigaon', 'Nagaon', 'Nalbari', 'Sivasagar', 'South Salmara Mankachar', 'Sonitpur', 'Tinsukia', 'Udalguri', 'West Karbi Anglong'],
    'Bihar': ['Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 'Bhagalpur', 'Bhojpur', 'Buxar', 'Darbhanga', 'East Champaran', 'Gaya', 'Gopalganj', 'Jamui', 'Jehanabad', 'Kaimur', 'Katihar', 'Khagaria', 'Kishanganj', 'Lakhisarai', 'Madhepura', 'Madhubani', 'Munger', 'Muzaffarpur', 'Nalanda', 'Nawada', 'Patna', 'Purnia', 'Rohtas', 'Saharsa', 'Samastipur', 'Saran', 'Sheikhpura', 'Sheohar', 'Sitamarhi', 'Siwan', 'Supaul', 'Vaishali', 'West Champaran'],
    'Chhattisgarh': ['Balod', 'Baloda Bazar', 'Balrampur', 'Bastar', 'Bemetara', 'Bijapur', 'Bilaspur', 'Dantewada', 'Dhamtari', 'Durg', 'Gariyaband', 'Janjgir-Champa', 'Jashpur', 'Kabirdham', 'Kanker', 'Kondagaon', 'Korba', 'Korea', 'Mahasamund', 'Mungeli', 'Narayanpur', 'Raigarh', 'Raipur', 'Rajnandgaon', 'Sukma', 'Surajpur', 'Surguja'],
    'Goa': ['North Goa', 'South Goa'],
    'Gujarat': ['Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha (Palanpur)', 'Bharuch', 'Bhavnagar', 'Botad', 'Chhota Udepur', 'Dahod', 'Dangs (Ahwa)', 'Devbhoomi Dwarka', 'Gandhinagar', 'Gir Somnath', 'Jamnagar', 'Junagadh', 'Kachchh', 'Kheda (Nadiad)', 'Mahisagar', 'Mehsana', 'Morbi', 'Narmada (Rajpipla)', 'Navsari', 'Panchmahal (Godhra)', 'Patan', 'Porbandar', 'Rajkot', 'Sabarkantha (Himmatnagar)', 'Surat', 'Surendranagar', 'Tapi (Vyara)', 'Vadodara', 'Valsad'],
    'Haryana': ['Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Gurugram (Gurgaon)', 'Hisar', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh', 'Nuh', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat', 'Yamunanagar'],
    'Himachal Pradesh': ['Bilaspur', 'Chamba', 'Hamirpur', 'Kangra', 'Kinnaur', 'Kullu', 'Lahaul & Spiti', 'Mandi', 'Shimla', 'Sirmaur (Sirmour)', 'Solan', 'Una'],
    'Jharkhand': ['Bokaro', 'Chatra', 'Deoghar', 'Dhanbad', 'Dumka', 'East Singhbhum', 'Garhwa', 'Giridih', 'Godda', 'Gumla', 'Hazaribag', 'Jamtara', 'Khunti', 'Koderma', 'Latehar', 'Lohardaga', 'Pakur', 'Palamu', 'Ramgarh', 'Ranchi', 'Sahibganj', 'Seraikela-Kharsawan', 'Simdega', 'West Singhbhum'],
    'Karnataka': ['Bagalkot', 'Ballari (Bellary)', 'Belagavi (Belgaum)', 'Bengaluru (Bangalore) Rural', 'Bengaluru (Bangalore) Urban', 'Bidar', 'Chamarajanagar', 'Chikballapur', 'Chikkamagaluru (Chikmagalur)', 'Chitradurga', 'Dakshina Kannada', 'Davangere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Kalaburagi (Gulbarga)', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru (Mysore)', 'Raichur', 'Ramanagara', 'Shivamogga (Shimoga)', 'Tumakuru (Tumkur)', 'Udupi', 'Uttara Kannada (Karwar)', 'Vijayapura (Bijapur)', 'Yadgir'],
    'Kerala': ['Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad'],
    'Madhya Pradesh': ['Agar Malwa', 'Alirajpur', 'Anuppur', 'Ashoknagar', 'Balaghat', 'Barwani', 'Betul', 'Bhind', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Dhar', 'Dindori', 'Guna', 'Gwalior', 'Harda', 'Hoshangabad', 'Indore', 'Jabalpur', 'Jhabua', 'Katni', 'Khandwa', 'Khargone', 'Mandla', 'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch', 'Panna', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shajapur', 'Sheopur', 'Shivpuri', 'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain', 'Umaria', 'Vidisha'],
    'Maharashtra': ['Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara', 'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai City', 'Mumbai Suburban', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad', 'Palghar', 'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal'],
    'Manipur': ['Bishnupur', 'Chandel', 'Churachandpur', 'Imphal East', 'Imphal West', 'Jiribam', 'Kakching', 'Kamjong', 'Kangpokpi', 'Noney', 'Pherzawl', 'Senapati', 'Tamenglong', 'Tengnoupal', 'Thoubal', 'Ukhrul'],
    'Meghalaya': ['East Garo Hills', 'East Jaintia Hills', 'East Khasi Hills', 'North Garo Hills', 'Ri Bhoi', 'South Garo Hills', 'South West Garo Hills', 'South West Khasi Hills', 'West Garo Hills', 'West Jaintia Hills', 'West Khasi Hills'],
    'Mizoram': ['Aizawl', 'Champhai', 'Kolasib', 'Lawngtlai', 'Lunglei', 'Mamit', 'Saiha', 'Serchhip'],
    'Nagaland': ['Dimapur', 'Kiphire', 'Kohima', 'Longleng', 'Mokokchung', 'Mon', 'Peren', 'Phek', 'Tuensang', 'Wokha', 'Zunheboto'],
    'Odisha': ['Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 'Deogarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghapur', 'Jajpur', 'Jharsuguda', 'Kalahandi', 'Kandhamal', 'Kendrapara', 'Kendujhar (Keonjhar)', 'Khordha', 'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangpur', 'Nayagarh', 'Nuapada', 'Puri', 'Rayagada', 'Sambalpur', 'Sonepur', 'Sundargarh'],
    'Punjab': ['Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Ferozepur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Mansa', 'Moga', 'Muktsar', 'Nawanshahr (Shahid Bhagat Singh Nagar)', 'Pathankot', 'Patiala', 'Rupnagar', 'Sahibzada Ajit Singh Nagar (Mohali)', 'Sangrur', 'Tarn Taran'],
    'Rajasthan': ['Ajmer', 'Alwar', 'Banswara', 'Baran', 'Barmer', 'Bharatpur', 'Bhilwara', 'Bikaner', 'Bundi', 'Chittorgarh', 'Churu', 'Dausa', 'Dholpur', 'Dungarpur', 'Hanumangarh', 'Jaipur', 'Jaisalmer', 'Jalore', 'Jhalawar', 'Jhunjhunu', 'Jodhpur', 'Karauli', 'Kota', 'Nagaur', 'Pali', 'Pratapgarh', 'Rajsamand', 'Sawai Madhopur', 'Sikar', 'Sirohi', 'Sri Ganganagar', 'Tonk', 'Udaipur'],
    'Sikkim': ['East Sikkim', 'North Sikkim', 'South Sikkim', 'West Sikkim'],
    'Tamil Nadu': ['Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kanchipuram', 'Kanyakumari', 'Karur', 'Krishnagiri', 'Madurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukudi (Tuticorin)', 'Tiruchirappalli', 'Tirunelveli', 'Tirupathur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore', 'Viluppuram', 'Virudhunagar'],
    'Telangana': ['Adilabad', 'Bhadradri Kothagudem', 'Hyderabad', 'Jagtial', 'Jangaon', 'Jayashankar Bhoopalpally', 'Jogulamba Gadwal', 'Kamareddy', 'Karimnagar', 'Khammam', 'Komaram Bheem Asifabad', 'Mahabubabad', 'Mahabubnagar', 'Mancherial', 'Medak', 'Medchal', 'Nagarkurnool', 'Nalgonda', 'Nirmal', 'Nizamabad', 'Peddapalli', 'Rajanna Sircilla', 'Rangareddy', 'Sangareddy', 'Siddipet', 'Suryapet', 'Vikarabad', 'Wanaparthy', 'Warangal (Rural)', 'Warangal (Urban)', 'Yadadri Bhuvanagiri'],
    'Tripura': ['Dhalai', 'Gomati', 'Khowai', 'North Tripura', 'Sepahijala', 'South Tripura', 'Unakoti', 'West Tripura'],
    'Uttar Pradesh': ['Agra', 'Aligarh', 'Allahabad', 'Ambedkar Nagar', 'Amethi (Chatrapati Sahuji Mahraj Nagar)', 'Amroha (J.P. Nagar)', 'Auraiya', 'Azamgarh', 'Baghpat', 'Bahraich', 'Ballia', 'Balrampur', 'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Bhadohi', 'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli', 'Chitrakoot', 'Deoria', 'Etah', 'Etawah', 'Faizabad', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur (Panchsheel Nagar)', 'Hardoi', 'Hathras', 'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 'Kanshiram Nagar (Kasganj)', 'Kaushambi', 'Kushinagar (Padrauna)', 'Lakhimpur - Kheri', 'Lalitpur', 'Lucknow', 'Maharajganj', 'Mahoba', 'Mainpuri', 'Mathura', 'Mau', 'Meerut', 'Mirzapur', 'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'RaeBareli', 'Rampur', 'Saharanpur', 'Sambhal (Bhim Nagar)', 'Sant Kabir Nagar', 'Shahjahanpur', 'Shamali (Prabuddh Nagar)', 'Shravasti', 'Siddharth Nagar', 'Sitapur', 'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi'],
    'Uttarakhand': ['Almora', 'Bageshwar', 'Chamoli', 'Champawat', 'Dehradun', 'Haridwar', 'Nainital', 'Pauri Garhwal', 'Pithoragarh', 'Rudraprayag', 'Tehri Garhwal', 'Udham Singh Nagar', 'Uttarkashi'],
    'West Bengal': ['Alipurduar', 'Bankura', 'Birbhum', 'Cooch Behar', 'Dakshin Dinajpur (South Dinajpur)', 'Darjeeling', 'Hooghly', 'Howrah', 'Jalpaiguri', 'Jhargram', 'Kalimpong', 'Kolkata', 'Malda', 'Murshidabad', 'Nadia', 'North 24 Parganas', 'Paschim Medinipur (West Medinipur)', 'Paschim (West) Burdwan (Bardhaman)', 'Purba Burdwan (Bardhaman)', 'Purba Medinipur (East Medinipur)', 'Purulia', 'South 24 Parganas', 'Uttar Dinajpur (North Dinajpur)'],
}
stateList = {
    "Andhra Pradesh": 13, "Arunachal Pradesh": 26, "Assam": 34, "Bihar": 38, "Chhattisgarh": 28, "Goa": 2,
    "Gujarat": 33, "Haryana": 22, "Himachal Pradesh": 12, "Jharkhand": 24, "Karnataka": 31, "Kerala": 14, "Madhya Pradesh": 52,
    "Maharashtra": 36, "Manipur": 16, "Meghalaya": 12, "Mizoram": 8, "Nagaland": 11, "Odisha": 30, "Punjab": 23, "Rajasthan": 33,
    "Sikkim": 4, "Tamil Nadu": 38, "Telangana": 33, "Tripura": 8, "Uttar Pradesh": 75, "Uttarakhand": 13, "West Bengal": 23
}

stateRtoCode = {
    "Andhra Pradesh": "AP", "Arunachal Pradesh": "AR", "Assam": "AS", "Bihar": "BR", "Chhattisgarh": "CG", "Goa": "GA",
    "Gujarat": "GJ", "Haryana": "HR", "Himachal Pradesh": "HP", "Jharkhand": "JH", "Karnataka": "KA", "Kerala": "KL", "Madhya Pradesh": "MP",
    "Maharashtra": "MH", "Manipur": "MN", "Meghalaya": "ML", "Mizoram": "MZ", "Nagaland": "NL", "Odisha": "OD", "Punjab": "PN", "Rajasthan": "RJ",
    "Sikkim": "SK", "Tamil Nadu": "TN", "Telangana": "TS", "Tripura": "TR", "Uttar Pradesh": "UP", "Uttarakhand": "UK", "West Bengal": "WB"
}

stateRtoCount = {
    "Andhra Pradesh": 38, "Arunachal Pradesh": 16, "Assam": 34, "Bihar": 11, "Chhattisgarh": 30, "Goa": 6,
    "Gujarat": 38, "Haryana": 98, "Himachal Pradesh": 80, "Jharkhand": 24, "Karnataka": 71, "Kerala": 86, "Madhya Pradesh": 54,
    "Maharashtra": 50, "Manipur": 8, "Meghalaya": 14, "Mizoram": 9, "Nagaland": 8, "Odisha": 35, "Punjab": 99, "Rajasthan": 53,
    "Sikkim": 8, "Tamil Nadu": 96, "Telangana": 36, "Tripura": 8, "Uttar Pradesh": 96, "Uttarakhand": 19, "West Bengal": 78
}

# Generate random number between 0 to 22
# num = random.randint(0,469)
# print(firstMaleName[num])

actfirName = ""
actlstName = ""
actfullName = ""
actMobileNumber = 0
upiNumber = 0


def firstNameGenerator():
    """
    This function generates random user's first name.
            Returns:
                    Random First Name of a user (str)
    """
    firstNameIndex = randint(0, len(firstMaleName)-1)
    global actfirName

    actfirName = firstMaleName[firstNameIndex]
    return actfirName


def lastNameGenerator():
    """
    This function generates random user's last name.
            Returns:
                    Random Last Name of a user (str)
    """
    lastNameIndex = randint(0, len(title)-1)
    global actlstName

    actlstName = title[lastNameIndex]
    return actlstName


def fullNameGenerator():
    """
      This function generates random user's full name.
        Returns:
          Random full Name of a user (str)
    """
    global actfirName
    global actlstName
    if actfirName == "":
        if actlstName == "":
            lstNme = lastNameGenerator()
            fstNme = firstNameGenerator()
            actFullName = fstNme + " " + lstNme

        else:
            fstNme = firstNameGenerator()
            actFullName = fstNme + " " + actlstName

    elif actlstName == "":
        lstNme = lastNameGenerator()
        actFullName = actfirName + " " + lstNme
    else:
        actFullName = actfirName + " " + actlstName
    return actFullName


def mobileNumberGenerator():
    """
      This function generates random mobile number.
        Returns:
          Random mobile number (number)
    """
    global actMobileNumber
    actMobileNumber = randint(6000000000, 9999999999)
    return actMobileNumber


def aadharNumberGenerator():
    """
      This function generates aadharnumber of a person
        Returns:
          Random aadharnumber (number)
    """
    aadharNumber = randint(100000000000, 999999999999)
    return aadharNumber


def emailIdGenerator():
    """
      This function generates random emailid of a person
        Returns:
          Random emailid (string)
    """
    emlNumber = randint(1000, 9999)
    domain = emlDomain[randint(0, len(emlDomain)-1)]
    if actfirName == "":
        firstNameGenerator()
    emailId = actfirName+str(emlNumber)+'@'+domain
    return emailId


def userIdGenerator():
    """
      This function generates random userId for a person
        Returns:
          Random userId (string)
    """
    if actfirName == "":
        firstNameGenerator()
    userIdNum = randint(1000, 9999)
    userId = actfirName + str(userIdNum)
    return userId


def passwordGenerator(length):
    """
      This function generates random password for a person
        Returns:
          Random password (string)
    """
    all = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.sample(all, length))
    return password


def upiIdGenerator():
    """
      This function generates random upi for a person
        Returns:
          Random upi id (string)
    """
    global actMobileNumber
    global upiNumber
    if actMobileNumber == 0:
        upiNumber = mobileNumberGenerator()
        upiCmpny = upiDomain[randint(0, len(upiDomain)-1)]
        upiNumber = str(actMobileNumber)+upiCmpny
    else:
        upiCmpny = upiDomain[randint(0, len(upiDomain)-1)]
        upiNumber = str(actMobileNumber)+upiCmpny
    return upiNumber


def hairColorGenerator():
    """
      This function generates random hair of a person
        Returns:
          Random hair color (string)
    """
    haircolor = hairColor[randint(0, len(hairColor)-1)]
    return haircolor


def genderGenerator():
    """
      This function generates random gender of a person
        Returns:
          Random gender (string)
    """
    genderOfPerson = gender[randint(0, len(gender)-1)]
    return genderOfPerson


def eyeColorGenerator():
    """
      This function generates random eyecolor of a person
        Returns:
          Random eyecolor (string)
    """
    eyecolorOfPerson = eyeColor[randint(0, len(eyeColor)-1)]
    return eyecolorOfPerson


def bloodGroupGenerator():
    """
      This function generates random blood group of a person
        Returns:
          Random blood group (string)
    """
    bloodgrpOfPerson = bloodGroup[randint(0, len(bloodGroup)-1)]
    return bloodgrpOfPerson


def skinColorGenerator():
    """
      This function generates random skin color of a person
        Returns:
          Random skin color (string)
    """
    sknClr = skinColor[randint(0, len(skinColor)-1)]
    return sknClr


def weightGenerator():
    """
      This function generates random weight of a person
        Returns:
          Random weight (number)
    """
    wt = randint(30, 100)
    return wt


def panCardId():
    """
      This function generates random pancard number of a person
        Returns:
          Random pancard number (string)
    """
    global actlstName
    result = ""
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    panNo=""
    for i in range(3):
      result += characters[randint(0,len(characters)-1)]
    if actlstName == "":
      lastNameGenerator()
      print(actlstName)
      lastNamefirstChar = actlstName[0]
      randNum = randint(1000,9999)
      lstChar = characters[randint(0,len(characters)-1)]
      panNo = result + "P" + lastNamefirstChar + str(randNum) + lstChar
    else:
      lastNamefirstChar = actlstName[0]
      randNum = randint(1000,9999)
      lstChar = characters[randint(0,len(characters)-1)]
      panNo = result + "P" + lastNamefirstChar + str(randNum) + lstChar
    return panNo

def passportNumber():
    """
      This function generates random passport number of a person
        Returns:
          Random passport number (string)
    """
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result =characters[randint(0,len(characters)-1)]
    num = str(randint(100000000,999999999))
    passNo = result + num
    return passNo

def financialCardGenerator():
    """
      This function generates random financial card details of a person
        Returns:
          Random financial card details [string, number, string, number]
    """
    global actfullName
    if actfullName =="":
      actfullName = fullNameGenerator()
      validMnth = randint(1,12)
      validYr  = randint(2023, 2028)
      cvv = randint(100, 999)
      visaElectronNum  = randint(4101110010111111, 4999999999999999)
      validThru = str(validMnth) + "/" + str(validYr)
      actCardFullDetails = [actfullName, visaElectronNum, validThru, cvv]
    else:
      validMnth = randint(1,12)
      validYr  = randint(2023, 2028)
      cvv = randint(100, 999)
      visaElectronNum  = randint(4101110010111111, 4999999999999999)
      validThru = str(validMnth) + "/" + str(validYr)
      actCardFullDetails = [actfullName, visaElectronNum, validThru, cvv]
    return actCardFullDetails