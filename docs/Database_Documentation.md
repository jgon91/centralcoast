Database documentation:
	The database documentation have all the classes in the database followed by all the attributes and a small description
	and some information of the type of the attribute in the database. If you add a new attribute or table in the database make sure to use the following model:
		########## New: ##########
		TYPE_NEW_FIELD_HERE
		##########################
	If you wanto to delete:
		######## Delete: ########
		TYPE_NEW_FIELD_HERE
		#########################
	This model was adopted to show all the people working on the database or the functions that a new attribute was added and some functions/forms will have to be changed. You are only allowed to take this off once all the necessary modifications were done.

Manufacturer
	name 					Manufacturer’s name - CHARFIELD(20)

ManufacturerModel
	manufacturer			Manufacturer ID - INT FOREIGN KEY REFERENCES Manufacturer	
	model					Model number - CHARFIELD(10)

RepairShop
	name					Contact name for repair shop - CHARFIELD(20)
	number					Contact number for repair shop - CHARFIELD(14)
	address					Contact address for repair shop - CHARFIELD(150)

Shop
	name					Contact name for shop - CHARFIELD(20)
	number					Contact number for shop - CHARFIELD(14)
	address					Contact address for shop - CHARFIELD(150)

EquipmentCategory
	name 					Category name - CHARFIELD(25)

EquipmentType
	category 				Category identification number -  INT FOREIGN KEY
	name					Type name - CHARFIELD(25)

Machine
	m_id 					Identification number - INT PRIMARY KEY AUTO_INCREMENT
	manufacturer_model		Model identification number - INT FOREIGN KEY
	repair_shop				repair_office ID - INT FOREIGN KEY
	shop					Where machine was purchased ID - INT FOREIGN KEY
	qr_code 				QR code number - CHARFIELD(10)
	nickname				Machine nickname - CHARFIELD(20)
	asset_number	 		Customer’s property number - CHARFIELD(15) UNIQUE NOT NULL
	serial_number: 			Machine serial number - CHARFIELD(25)
	horsepower:				Engine output power - INT
	hitch_capacity			Hydraulic Power - INT
	hitch_category			Size of the hitch - CHOICES
	drawbar_category		Size of drawbar pin - CHOICES
	speed_range_min			Customer defined min speed- FLOAT
	speed_range_max			Customer defined max speed - FLOAT
	year_purchased			Year the machine as purchased - INT
	engine_hours			Total engine hours - INT
	service_interval		Interval time between services - INT (is it a average hours between work intervals?)
	base_cost				Purchase price of the equipment - FLOAT 
	m_type					Tracks or wheels - CHOICES
	front_tires				Size of front tire - CHARFIELD(20)
	rear_tires				Size of rear tire - CHARFIELD(20)
	steering				Manual or GPS - CHOICES
	operator_station		Cab or open - CHOICES
	status					Machine status - CHOICES
	hour_cost				Machine hour cost - FLOAT
	equipment_type			EquipmentType identification number - FOREIGN KEY
	photo					Path to the picture -  URL(200)

Implements
	manufacturer_model		Model identification number - INT FOREIGN KEY
	shop					Where implement was purchased - INT FOREIGN KEY
	repair_shop				repair_office ID- INT FOREIGN KEY
	qr_code					QR code number - CHARFIELD(10)
	nickname				Implement nickname - CHARFIELD(20)
	asset_number			Customer’s property number - CHARFIELD(15)
	serial_number: 			Machine serial number - CHARFIELD(25)
	horse_power_req			Minimum required horsepower - INT		
	hitch_capacity_req		Minimum tractor hitch lift capacity - INT
	hitch_category			Size of the hitch - CHOICES
	drawbar_category		Size of drawbar pin - CHOICES
	speed_range_min			Customer defined min speed- FLOAT
	speed_range_max			Customer defined max speed - FLOAT
	year_purchased			Year the implement has purchased - INT
	implement_hours			Total hours implement worked - INT
	service_interval		Interval time between services - INT
	base_cost				Purchase price of the equipment - FLOAT
	status					Implement status - CHOICES
	hour_cost				Implement hour cost - FLOAT
	equipment_type			EquipmentType identification number - FOREIGN KEY
	photo					Path until the picture -  URL(200)

Employee
	last_task				Foreign Key from task to tell us the last task the employee worked on
	company_id				Identification number by company - CHARFIELD(10)      
	qr_code					QR code number - CHARFIELD(10)
	first_name				Employee’s first name - CHARFIELD(15)
	last_name				Employee’s last name - CHARFIELD(15)
	start_date				Employee start date -  DATE
	hour_cost				Employee hour cost - FLOAT
	contact_number  		Contact number - CHARFIELD(14)
	permission_level		Clearance level of employee - INT CHOICES
	language				Employee comfortable language - CHOICES
	photo					Path until the picture - URL(200) -

EmployeeWithdrawn
	withdraw				Table identification number - INT PRIMARY KEY 
	employee				Employee identification - INT FOREIGN KEY
	date					Date of withdrawn - DATE

EmployeeAttendance
	employee				Employee Identification number - INT
	FOREIGN KEY
	date					Attendance day - DATE
	hour_started			Hour the swift started - TIME
	hour_ended				Hour the swift ended - TIME NULL
	signature				Digital signature of employee - CHARFIELD(5000)

Break
	attendance				EmployeeAttendance Identification Number - FOREIGN KEY
	start					Time when break started - TIME
	end						Time when break end - TIME NULL

Qualification
	description				Qualification Description - CHARFIELD(50)

Certification
	description				certification description - CHARFIELD(100)
	year					Year of certification - INTEGER

EmployeeQualification
	employee				Employee ID - INT  FOREIGN KEY 
	qualification			Qualification ID- INT  FOREIGN KEY
	q_level		 			Qualification level - INT CHOICES

EmployeeCertification
	employee				Employee ID -INT FOREIGN KEY
	certification			Certification ID - INT FOREIGN KEY 

MachineQualification
	machine					Identification number - INT FOREIGN KEY
	qualification			Qualification identification number - INT FOREIGN  KEY
	qualification_required	Qualification required - INT CHOICES
				

MachineCertification
machine						Identification number - INT FOREIGN KEY
certification				Certification  identification number - INT FOREIGN  KEY

	
ImplementQualification
implement					Identification number - INT FOREIGN KEY				
qualification				Qualification identification number - INT FOREIGN KEY
qualification_required		Qualification required - CHOICES

ImplementCertification
machine						Machine identification number - INT FOREIGN KEY
certification				Certification identification number - INT FOREIGN KEY

Field
	name					Name - CHARFIELD(50)
	organic 				is it organic - BOOLEAN (False = conventional)
	size					Field size - FLOAT (Acres)

GPS
	latitude				Latitude point - FLOAT	
	longitude				Longitude point - FLOAT

FieldLocalization
	field					Field identification number - INT FOREIGN KEY
	gps						GPS identification number- INT FOREIGN KEY

EmployeeLocalization
	employee				Employee identification number - INT FOREIGN KEY 
	e_time					Time of the localization - DATE
	latitude				Latitude point - FLOAT	
	longitude				Longitude point - FLOAT

TaskCategory
	description				Category of task - CHARFIELD(30)

Task
	field					Id of the field where the task will be performed - ForeignKey(Field)
	category				Task category - ForeignKey(TaskCategory)
	rate_cost				Cost of the task per hour - FloatField
	date_assigned			The date that this task was assigned - DateTimeField
	hours_prediction		How many hours it supposed take - FloatField
	description				Task description - CharField(max_length = 500)
	passes					Number of passes - IntegerField
	task_init				Actual time when the task was started - DateTimeField
	task_end				When the task was finished - DateTimeField
	status					Store the current status of the machine - IntegerField(choices)
	hours_spent				Hours spent on the task - FloatField
	pause_start				Store the start of a pause in the task - DateTimeField
	pause_end				Store the end of a pause that was started - DateTimeField
	pause_total				Total time of pauses - FloatField

EmployeeTask
	employee				Id of the employee performing the task - ForeignKey(Employee)
	task					Task to be performed - ForeignKey(Task)
	hours_spent				Hours spent by the employee in this task - FloatField
	start_time				Employee task initiation time - DateTimeField
	end_time				Employee task end time - DateTimeField

MachineTask
	task					Id of the task to be performed by the machine - ForeignKey(Task)
	machine					Id of the machine performing the task - ForeignKey(Machine)
	employee_task			Id of the EmployeeTask that will be using the machine and performing the task - ForeignKey(EmployeeTask)

ImplementTask
	task					Id of the task to be performed by the implement - ForeignKey(Task)
	machine					Id of the machine using the implement - ForeignKey(Machine)
	implement_id			Id of the Implement that will be used by the machine - ForeignKey(EmployeeTask)	

Appendix
	type					Type of appendix- CHARFIELD(20) e.g (fertilizer)-(pesticides)-(NONE)

AppendixTask
	appendix				Appendix Identification -  INT FOREIGN KEY 
	task					Task Identification - INT FOREIGN KEY
	quantity				Quantity used - INT
	brand					Appendix brand - CHARFIELD(20)

ServiceCategory
	service_category 		Category of service - CHARFIELD(30) (Engine change) - (Oil change) - (Filter change)

Service
	category				Type of service - SMALLINT FOREIGN KEY 
	date					Date of service - DATE
	done					Is the service done - BOOLEAN

MachineService
	machine					Machine identification number - INT COMPOSITE FOREIGN KEY
	service					Service identification number - INT COMPOSITE FOREIGN KEY
	description				Service description - CHARFIELD(200)
	done					Is the service done - BOOLEAN
	expected_date			Expected day to be finished - Date
	price					Service price - FLOAT

ImplementService
	implement				Machine identification number - INT FOREIGN  KEY
	service					Service identification number - INT FOREIGN KEY 
	description				Service description - CHARFIELD(200)
	expected_date			Expected day to be finished - Date
	done					Is the service done - BOOLEAN
	price					Service price - FLOAT


Question
	description 			Question which will be made - CHARFIELD(250)
	category				This field will differentiate the question into groups - int
	refers					This question is related to Machine or Implement - Choices

MachineChecklist
	question				Question identification number - FOREIGN KEY
	qrCode					QRCode referent of the equipment -  FOREIGN KEY
	employee 				Reference for employee - FOREIGN KEY
	answer 					If the answer is positive or negative - BOOLEAN
	note					Description of the problem -	CHARFIELD(200) NULL
	date					Date of the service - DATE 
	photo					Path until the picture - URL(200) NULL

ImplementChecklist
	question				Question identification number - FOREIGN KEY
	qrCode					QRCode referent of the equipment - FOREIGN KEY
	employee 				Reference for employee - FOREIGN KEY
	answer 					If the answer is positive or negative - BOOLEAN
	note					Description of the problem -	CHARFIELD(200) NULL
	date					Date of the service - DATE 
	photo					Path until the picture - URL(200) NULL