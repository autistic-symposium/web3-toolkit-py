import json


def solution(postContentString, deltasString):
		postContent = json.loads(postContentString)
		deltas = json.loads(deltasString)
    
    # -------------------------------------
    # Loop to each delta action from deltas.
    # -------------------------------------
		for delta in deltas:

				# ----------------------
        # Get delta action data.
        # ----------------------
				try:
						delta_type = delta['type']
						delta_pindex = delta['paragraphIndex']
            
            # ---------------------------------------
            # Check if delta paragraph index is valid.
            # ---------------------------------------
						if delta_pindex < 0 or delta_pindex >= len(postContent['paragraphs']):
								continue
            
				except (KeyError, IndexError) as e:
						continue
            
				# ------------------------------
        # Execute update paragraph delta.
        # ------------------------------
				if delta_type == 'updateParagraph':
						try:
								delta_paragraph_text = delta['paragraph']['text']
								postContent['paragraphs'][delta_pindex]['text'] = delta_paragraph_text

						except IndexError:
								continue
						
				# ----------------------------
        # Execute add paragraph delta.
        # ----------------------------
				elif delta_type == 'addParagraph':
						try:
								delta_paragraph = delta['paragraph']
								postContent['paragraphs'].insert(delta_pindex, delta_paragraph)
								
                # ------------------
                # Fix section index.
                # ------------------
								i = delta_pindex
								while i < len(postContent['sections'][delta_pindex:]) + 1:
										postContent['sections'][i]['startIndex'] +=  1
										i += 1
              
						except IndexError:
								continue
						
				# -------------------------------
        # Execute delete paragraph delta.
        # -------------------------------
				elif delta_type == 'deleteParagraph':
						try:
								postContent['paragraphs'].pop(delta_pindex)
								
                # ------------------
                # Fix section index.
                # ------------------
                
                # Fix section indexes after removal.
								i = delta_pindex 
								while i < len(postContent['sections'][delta_pindex:]) + 1:
										postContent['sections'][i]['startIndex'] -=  1
										i += 1
                
                # Remove any empty section.
								i = 1
								for i, section in enumerate(postContent['sections']):
										if section['startIndex'] <= 0:
												postContent['sections'].pop(i)

						except IndexError:
								continue

		# ------------------
    # Print out results.
    # ------------------
		try:
				# -------------------------------------------
    		# Extract sections and paragraph, after delta.
				# -------------------------------------------
				sections = postContent['sections']
				paragraphs = postContent['paragraphs']
                                 
				# ------------------------
        # Find all section indexes.
        # ------------------------
				section_indexes = set()
				for section in sections:
						section_indexes.add(section['startIndex'])
        
        # ---------------------------------------------------
        # Loop over paragraphs to create the resulting string.
        # ---------------------------------------------------
				res = []

				for i, paragraph in enumerate(paragraphs, start=1):

						if i == len(paragraphs):
								res.append(f'{paragraph["text"]}')
          
						elif i in section_indexes:
								res.append(f'{paragraph["text"]}\n-\n')
           
						else:
								res.append(f'{paragraph["text"]}\n')

		except (KeyError, ValueError) as e:
				print(f'Error: Input data is ill-formatted: {e}')

		return ''.join(res)
