Hướng dẫn sử dụng chương trình phân cụm mờ cùng với các tiêu chí đánh giá chất lượng phân cụm
Mã nguồn được viết bằng ngôn ngữ Python 3

1, Lưu ý
	
	+, Dữ liệu được import phải có định dạng .csv
	+, Hàng đầu tiên của file .csv nên là hàng tên các thuộc tính (nếu dữ liệu không có hàng thuộc tính xin vui lòng để trống)
	+, Dữ liệu có thể có nhãn hoặc không có nhãn, nếu có xin vui lòng để cột có nhãn dữ liệu ở cuối cùng (nhãn có thể là xâu ký tự hoặc số đều được)
	+, Dữ liệu có thể có cột ID hoặc không có, nếu có xin vui lòng để cột có ID dữ liệu ở đầu tiên (cột ID có thể là xâu ký tự hoặc số đều được)
	+, CỘt có nhãn dữ liệu sẽ tự động được convert sang dạng xâu ký tự.
	+, Các tiêu chí đánh giá ngoài chỉ được hiển thị nếu tập dữ liệu có cột chứa các nhãn tương ứng, và cột này phải nằm ở cuối data sets 

2, Chạy chương trình

2.1, Các thư viện cần cài dặt

	+, Cách 1: (nên sử dụng cách này), Cài đặt Anaconda để sử dụng Spyder (một Interactive Python): https://www.anaconda.com/
	+, Cách 2: Cần đảm bảo các gói numpy, scipy, tkinter, pandas đã được cài đặt
		sử dụng pip như sau: python3 -m pip install --user numpy scipy pandas tkinter

2.2, Chạy thử nghiệm;

	+, Chạy file test.py như các chương trình python thông thường
	
	+, Các yêu cầu cần nhập với người dùng:
		-, chọn file
		-, chọn y / n nếu có hoặc không có cột chứa nhãn dữ liệu
		-, chọn y / n nếu có hoặc không có cột chứa ID dữ liệu
		-, Chọn số lượng cụm: 1 < K < N (N là số điểm dữ liệu)
		-, Chọn số đủ bé cho điều kiện dừng: 0.0001 <= epsilon <= 0.001
		-, Chọn tham số m là tham số của thuật toán phân cụm mờ: 1.5 < m < 3.0



