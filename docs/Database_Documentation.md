
#####MANUFACTURE#######
Manufacturer
name             Manufacturer’s name - VARCHAR(20)
ManufacturerModel
manufacturer        
Manufacture 	identification number - INT FOREIGN KEY
                    REFERENCES Manufacturer    


#####MODEL#######
model            
Model number - VARCHAR(10) UNIQUE
RepairShop
name            Contact name for repair shop - VARCHAR(20)
number          Contact number for repair shop - VARCHAR(14)
address         Contact address for repair shop - VARCHAR(150)



#####SHOP#######
Shop
name            Contact name for shop - VARCHAR(20)
number        	Contact number for shop - VARCHAR(14)
address         Contact address for shop - VARCHAR(150)


######MACHINE####
Machine
m_id             Identification number - INT PRIMARY KEY 
                    AUTO_INCREMENT
manufacturer_model    Model identification number - INT FOREIGN KEY
repair_shop      repair_office ID - INT FOREIGN KEY
shop             Where machine was purchased ID - INT FOREIGN    
KEY
qr_code          QR code number - VARCHAR(10)
nickname         Machine nickname - VARCHAR(20)
asset_number     Customer’s property number - VARCHAR(15)
                UNIQUE NOT NULL
serial_number:   Machine serial number - VARCHAR(25)
horsepower:      Engine output power - INT
hitch_capacity   Hydraulic Power - INT
hitch_category   Size of the hitch - CHOICES
drawbar_category Size of drawbar pin - CHOICES
speed_range_min  Customer defined min speed- FLOAT
speed_range_max  Customer defined max speed - FLOAT
year_purchased   Year the machine as purchased - INT
engine_hours     Total engine hours - INT
service_interval Interval time between services - INT (is it a average 
                hours between work intervals?)
base_cost        Purchase price of the equipment - FLOAT 
m_type           Tracks or wheels - CHOICES
front_tires      Size of front tire - VARCHAR(20)
rear_tires       Size of rear tire - VARCHAR(20)
steering         Manual or GPS - CHOICES
operator_station Cab or open - CHOICES
status           Machine status - CHOICES
hour_cost        Machine hour cost - FLOAT
photo            Path to the picture -  URL(200)


####IMPLEMENTS######
Implements
manufacturer_model    Model identification number - INT FOREIGN KEY
shop           		  Where implement was purchased - INT FOREIGN KEY
repair_shop           repair_office ID- INT FOREIGN KEY
qr_code      	      QR code number - VARCHAR(10)
nickname     	      Implement nickname - VARCHAR(20)
asset_number       	  Customer’s property number - VARCHAR(15)
serial_number:        Machine serial number - VARCHAR(25)
horse_power_req       Minimum required horsepower - INT        
hitch_capacity_req    Minimum tractor hitch lift capacity - INT
hitch_category        Size of the hitch - CHOICES
drawbar_category      Size of drawbar pin - CHOICES
speed_range_min       Customer defined min speed- FLOAT
speed_range_max       Customer defined max speed - FLOAT
year_purchased        Year the implement has purchased - INT
implement_hours      Total hours implement worked - INT
service_interval     Interval time between services - INT
base_cost            Purchase price of the equipment - FLOAT
status               Implement status - CHOICES
hour_cost            Implement hour cost - FLOAT
photo                Path until the picture -  URL(200)



####EMLOYEEE####
Employee
company_id    	Identification number by company - VARCHAR(10)      
qr_code         QR code number - VARCHAR(10)
first_name      Employee’s first name - VARCHAR(15)
last_name       Employee’s last name - VARCHAR(15)
start_date      Employee start date -  DATE
hour_cost       Employee hour cost - FLOAT
contact_number  Contact number - VARCHAR(14)
permission_level   Clearance level of employee - INT CHOICES
language        Employee comfortable language - CHOICES
photo           Path until the picture - URL(200) -


####EMPLOYEEWITHDRAW
EmployeeWithdrawn
withdraw        Table identification number - INT PRIMARY KEY 
employee        Employee identification - INT FOREIGN KEY
date            Date of withdrawn - DATE


####EMPLOYEEATTENDANCE####
EmployeeAttendance
employee        Employee Identification number - INT
FOREIGN KEY
date            Attendance day - DATE
hour_started    Hour the swift started - TIME
hour_ended      Hour the swift ended - TIME NULL
break_one       Time when morning break started - TIME NULL
break_one_end   Time when morning break started - TIME NULL
break_two       Time when afternoon break started - TIME NULL
break_two_end   Time when afternoon break started - TIME NULL
break_three     Time when evening break started - TIME NULL
break_three_end Time when evening break started - TIME NULL



####QUALIFICATION#####
Qualification
description     Qualification Description - VARCHAR(50)


#####CERTIFICATION#####
Certification
category        certification category - SMALLINT
description     certification description - VARCHAR(100)
EmployeeQualification
employee        Employee ID - INT  FOREIGN KEY 
qualification   Qualification ID- INT  FOREIGN KEY
q_level         Qualification level - INT CHOICES


####EMPLOYEECERTIFICATION####
EmployeeCertification
employee        Employee ID -INT FOREIGN KEY
certification   Certification ID - INT FOREIGN KEY 



####MACHINEQUALIFICATION####
MachineQualification
machine        Identification number - INT FOREIGN KEY
qualification  Qualification identification number - INT FOREIGN  KEY
qualification_required    Qualification required - INT CHOICES
                

####MACHINE CERTIFICATION####
Machine Certification
machine        Identification number - INT FOREIGN KEY
certification  Certification  identification number - INT FOREIGN  KEY

####IMPLEMENTQUALIFICATION####
ImplementQualification
implement        Identification number - INT FOREIGN KEY
                    
####QUALIFICATION####
qualification        
Qualification   identification number - INT 
				FOREIGN KEY
qualification_required    Qualification required - CHOICES

####IMPLEMENTCERTIFICATION####
ImplementCertification
machine        Machine identification number - INT FOREIGN KEY
certification  Certification identification number - INT FOREIGN KEY

####FIELD####
Field
name            Name - VARCHAR(50)
organic         is it organic - BOOLEAN (False = 
                conventional)
size            Field size - FLOAT (Acres)
GPS
latitude        Latitude point - FLOAT    
longitude       Longitude point - FLOAT
FieldLocalization
field           Field identification number - INT FOREIGN KEY
gps             GPS identification number- INT FOREIGN KEY 
EmployeeLocalization
employee        Employee identification number - INT FOREIGN KEY 
e_time          Time of the localization - DATE
latitude        Latitude point - FLOAT    
longitude       Longitude point - FLOAT


####TASKCATEGORY####
TaskCategory
description     Category of task - VARCHAR(30)

Task
field           Id of task - INT FOREIGN KEY FROM FIELD
category        Task category - INT FOREIGN KEY
rate_cost       Cost of the task per hour - FLOAT 
hours_spent     Hours spent on the task - FLOAT
hours_prediction   How many hours it supposed take - FLOAT
description     Task description - VARCHAR(500)
passes          Number of passes - INT
t_date          the date that this task was assigned - Date
accomplished    if the task is done - BOOLEAN
approval        Does the task have manager approval - Choices
EmployeeTask
employee        Employee ID - INT FOREIGN KEY
task            Task ID - INT     COMPOSITE FOREIGN KEY
task_init       Task initiation - DATE (UNIX_TIMESTAMP(now()))
hours_spent     Hours spent in this task- SMALLINT
substituition   Substituition happened? - BOOLEAN
TaskImplementMachine
task            Task ID - INT     FOREIGN KEY
machine         Machine ID - INT FOREIGN KEY
implement       Implement ID - INT COMPOSITE KEY
machine         Is this just machine machine - BOOLEAN
Appendix
type            Type of appendix- VARCHAR(20) 
e.g (fertilizer)-(pesticides)-(NONE)
AppendixTask
appendix        Appendix Identification -  INT FOREIGN KEY 
task            Task Identification - INT FOREIGN KEY
quantity        Quantity used - INT
brand           Appendix brand - VARCHAR(20)
ServiceCategory
service_category Category of service - VARCHAR(30) (Engine change) -
                (Oil change) - (Filter change)

####SERVICE####
Service
category        Type of service - SMALLINT FOREIGN KEY 
date            Date of service - DATE
done            Is the service done - BOOLEAN



####MACHINESERVICE
MachineService
machine         Machine identification number - INT COMPOSITE 
				FOREIGN  KEY
service         Service identification number - INT COMPOSITE 
				FOREIGN KEY
description     Service description - VARCHAR(200)
done            Is the service done - BOOLEAN
expected_date   Expected day to be finished - Date
price           Service price - FLOAT


####IMPLEMENTSERVICE####
ImplementService
implement       Machine identification number - INT FOREIGN  KEY
service         Service identification number - INT FOREIGN KEY 
descriptio      Service description - VARCHAR(200)
expected_date   Expected day to be finished - Date
done            Is the service done - BOOLEAN
price           Service price - FLOAT


####QUESTION####
Question
description    Question which will be made - VARCHAR(250)
category       This field will differentiate the question into groups - int


####EQUIPMENTCHECKLIST####
EquipmentChecklist
question       Question identification number - INT FOREIGN KEY
qrCode         QRCode referent of the equipment - VARCHAR(10) 
answer         If the answer is positive or negative - BOOLEAN
note           Description of the problem -VARCHAR(200) NULL
date           Date of the service - DATE 
photo          Path until the picture - URL(200) NULL








    
