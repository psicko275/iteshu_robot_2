define hokuyolaser ranger
(
	sensor
	( 			
		# laser-specific properties
		# factory settings for LMS200	
		range [ 0.0  5.0 ]  #I changed this line from 30 meters
		fov 270.0 #180
		samples 721
	)

	# generic model properties
	color "blue"
	size [ 0.07 0.07 0.05 ] # dimensions from LMS200 data sheet	
)



