targetImg = imread('fishes.jpg');
targetImg = im2double(targetImg);
img_GrayScale = rgb2gray(targetImg);

scales = 10; %number of scales
sigma = 2; %value of sigma
k = sqrt(sqrt(2)); %scale multiplication constant  
threshold = 0.010; %threshold
% Select n=1 for DOG
% Select n=2 for LOG
n = 2; 
scaleSpace3D = detectBlobs( img_GrayScale, scales, sigma, k, threshold, n ); 

j = 1;


ScaleRadii = zeros(1,scales); 
while j <= scales
    ScaleRadii(j) =  sqrt(2) * sigma * k^(j-1);
    j = j+1;
end

i = 1;
blobMarkers = [];
while i <= scales
    %find indices in the scale slice where the pixel value is not 0
    [newMarkerRows, newMarkerCols] = find(scaleSpace3D(:,:,i));
    
    newMarkers = [newMarkerCols'; newMarkerRows'];
    newMarkers(3,:) = ScaleRadii(i);
     
    blobMarkers = [blobMarkers; newMarkers'];   
    i = i + 1;
end

xPos = blobMarkers(:,1); %col positions
yPos = blobMarkers(:,2); %row positions
radius = blobMarkers(:,3); %radii

show_all_circles(img_GrayScale, xPos, yPos, radius, 'r', 2);
