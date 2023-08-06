	c=np.zeros((len(times),3),dtype='float') 						#creation of matrix that will hold the concentrations
	g=gauss(times,sigma=pardf['resolution']/FWHM,mu=pardf['t0']) 	#creating the gaussian pulse that will "excite" our sample
	sub_steps=10 													#defining how many extra steps will be taken between the main time_points
	for i in range(1,len(times)):									#iterate over all timepoints
		dc=np.zeros((3,1),dtype='float')							#the initial change for each concentration, the "3" is representative of how many changes there will be
		dt=(times[i]-times[i-1])/(sub_steps)						# as we are taking smaller steps the time intervals need to be adapted
		c_temp=c[i-1,:]												#temporary matrix holding the changes (needed as we have sub steps and need to check for zero in the end)
		for j in range(int(sub_steps)):
			dc[0]=-pardf['k0']*dt*c_temp[0]-pardf['k2']*dt*c_temp[0]+g[i]*dt					
			dc[1]=pardf['k0']*dt*c_temp[0]-pardf['k1']*dt*c_temp[1]
			dc[2]=pardf['k1']*dt*c_temp[1]+pardf['k2']*dt*c_temp[0]
			for b in range(c.shape[1]):
				c_temp[b] =np.nanmax([(c_temp[b]+dc[b]),0.])		#check that nothing will be below 0 (concentrations)
		c[i,:] =c_temp												#store the temporary concentrations into the main matrix
	c=pandas.DataFrame(c,index=times)								#write back the right indexes
	c.index.name='time'												#and give it a name
	c.columns=['A','B','Inf']	