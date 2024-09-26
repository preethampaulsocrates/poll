from flask import Flask, request, jsonify, render_template
from collections import Counter

app = Flask(__name__)

# Dictionary to hold vote counts for options A, B, C, D
vote_counts = Counter({'A': 0, 'B': 0, 'C': 0, 'D': 0})

# Route for submitting votes
@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    data = request.get_json()

    # Validate the vote
    if not data.get('option') or data['option'] not in ['A', 'B', 'C', 'D']:
        return jsonify({'message': 'Invalid option selected'}), 400

    # Increment the vote count for the selected option
    vote_counts[data['option']] += 1

    return jsonify({'message': 'Vote submitted successfully!'}), 200

# Route to get vote percentages for admin
@app.route('/poll_results', methods=['GET'])
def poll_results():
    total_votes = sum(vote_counts.values())
    if total_votes == 0:
        return jsonify({
            'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0
        })

    # Calculate percentages
    percentages = {key: (count / total_votes) * 100 for key, count in vote_counts.items()}
    
    return jsonify(percentages)

# Route to serve the audience poll page
@app.route('/audience_poll')
def audience_poll():
    return render_template('audience_poll.html')

# Route to serve the admin poll results page
@app.route('/admin_poll')
def admin_poll():
    return render_template('admin_poll.html')

if __name__ == '__main__':
    app.run(debug=True)
